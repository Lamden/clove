from datetime import datetime, timedelta, timezone
import struct

from bitcoin.core import CMutableTransaction, CMutableTxOut, b2lx, b2x, script, x
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress

from clove.constants import SIGNATURE_SIZE
from clove.network.bitcoin.wallet import BitcoinWallet
from clove.utils.bitcoin import auto_switch_params, to_base_units
from clove.utils.hashing import generate_secret_with_hash


class BitcoinTransaction(object):
    '''Bitcoin transaction object.'''

    @auto_switch_params(1)
    def __init__(self, network, recipient_address: str, value: float, solvable_utxo: list, tx_locktime: int=0):
        self.recipient_address = recipient_address
        self.value = value
        self.network = network
        self.symbol = network.default_symbol

        self.validate_address()

        self.solvable_utxo = solvable_utxo
        self.utxo_value = sum(utxo.value for utxo in self.solvable_utxo)
        self.tx_in_list = [utxo.tx_in for utxo in self.solvable_utxo]
        self.tx_out_list = []

        self.tx = None
        self.tx_locktime = tx_locktime
        self.fee = 0.0
        self.fee_per_kb = 0.0

    def validate_address(self):
        if not self.network.is_valid_address(self.recipient_address):
            raise ValueError('Given recipient address is invalid.')

    def build_outputs(self):
        self.tx_out_list = [
            CMutableTxOut(to_base_units(self.value), CBitcoinAddress(self.recipient_address).to_scriptPubKey())
        ]

    def add_fee_and_sign(self, default_wallet=None):
        """Signing transaction and adding fee under the hood."""

        # signing the transaction for the first time to get the right transaction size
        self.sign(default_wallet)

        # adding fee based on transaction size (this will modify the transaction)
        self.add_fee()

        # signing the modified transaction
        self.sign(default_wallet)

    def sign(self, default_wallet: BitcoinWallet =None):
        """Signing transaction using the wallet object."""

        for tx_index, tx_in in enumerate(self.tx.vin):
            utxo = self.solvable_utxo[tx_index]
            wallet = utxo.wallet or default_wallet

            if wallet is None:
                raise RuntimeError('Cannot sign transaction without a wallet.')

            tx_script = utxo.parsed_script
            if utxo.contract:
                sig_hash = script.SignatureHash(
                    script.CScript.fromhex(utxo.contract),
                    self.tx,
                    tx_index,
                    script.SIGHASH_ALL
                )
            else:
                sig_hash = script.SignatureHash(
                    tx_script,
                    self.tx,
                    tx_index,
                    script.SIGHASH_ALL
                )
            sig = wallet.private_key.sign(sig_hash) + struct.pack('<B', script.SIGHASH_ALL)
            script_sig = [sig, wallet.private_key.pub] + utxo.unsigned_script_sig
            tx_in.scriptSig = script.CScript(script_sig)

            VerifyScript(
                tx_in.scriptSig,
                tx_script,
                self.tx,
                tx_index,
                (SCRIPT_VERIFY_P2SH,)
            )

    def create_unsigned_transaction(self):
        assert self.utxo_value >= self.value, 'You want to spend more than you\'ve got. Add more UTXO\'s.'
        self.build_outputs()
        self.tx = CMutableTransaction(self.tx_in_list, self.tx_out_list, nLockTime=self.tx_locktime)

    def publish(self):
        return self.network.publish(self.raw_transaction)

    @property
    def size(self) -> int:
        """Returns the size of a transaction represented in bytes."""
        return len(self.tx.serialize())

    def calculate_fee(self, add_sig_size=False):
        """Calculating fee for given transaction based on transaction size and estimated fee per kb."""
        if not self.fee_per_kb:
            self.fee_per_kb = self.network.get_current_fee_per_kb()
        size = self.size
        if add_sig_size:
            size += len(self.tx_in_list) * SIGNATURE_SIZE
        self.fee = round((self.fee_per_kb / 1000) * size, 8)

    def add_fee(self):
        """Adding fee to the transaction by decreasing 'change' transaction."""
        if not self.fee:
            self.calculate_fee()
        fee_in_satoshi = to_base_units(self.fee)
        if self.tx.vout[0].nValue < fee_in_satoshi:
            raise RuntimeError('Cannot subtract fee from transaction. You need to add more input transactions.')
        self.tx.vout[0].nValue -= fee_in_satoshi

    @property
    def raw_transaction(self):
        return b2x(self.tx.serialize())

    @property
    def address(self):
        return b2lx(self.tx.GetHash())

    def show_details(self):
        return {
            'transaction': self.raw_transaction,
            'transaction_address': self.address,
            'fee': self.fee,
            'fee_per_kb': self.fee_per_kb,
            'fee_per_kb_text': f'{self.fee_per_kb:.8f} {self.symbol} / 1 kB',
            'fee_text': f'{self.fee:.8f} {self.symbol}',
            'recipient_address': self.recipient_address,
            'size': self.size,
            'size_text': f'{self.size} bytes',
            'value': self.value,
            'value_text': f'{self.value:.8f} {self.symbol}',
        }


class BitcoinAtomicSwapTransaction(BitcoinTransaction):
    '''Bitcoin atomic swap object.'''
    init_hours = 48
    participate_hours = 24

    def __init__(
        self,
        network,
        sender_address: str,
        recipient_address: str,
        value: float,
        solvable_utxo: list,
        secret_hash: str=None,
        tx_locktime: int=0
    ):
        self.sender_address = sender_address
        super().__init__(network, recipient_address, value, solvable_utxo, tx_locktime)
        self.secret = None
        self.secret_hash = x(secret_hash) if secret_hash else None
        self.locktime = None
        self.contract = None

    def validate_address(self):
        invalid_recipient = not self.network.is_valid_address(self.recipient_address)
        invalid_sender = not self.network.is_valid_address(self.sender_address)
        if invalid_recipient and invalid_sender:
            raise ValueError('Given recipient and sender addresses are invalid.')
        elif invalid_recipient:
            raise ValueError('Given recipient address is invalid.')
        elif invalid_sender:
            raise ValueError('Given sender address is invalid.')

    def build_atomic_swap_contract(self):
        self.contract = script.CScript([
            script.OP_IF,
            script.OP_RIPEMD160,
            self.secret_hash,
            script.OP_EQUALVERIFY,
            script.OP_DUP,
            script.OP_HASH160,
            CBitcoinAddress(self.recipient_address),
            script.OP_ELSE,
            int(self.locktime.replace(tzinfo=timezone.utc).timestamp()),
            script.OP_CHECKLOCKTIMEVERIFY,
            script.OP_DROP,
            script.OP_DUP,
            script.OP_HASH160,
            CBitcoinAddress(self.sender_address),
            script.OP_ENDIF,
            script.OP_EQUALVERIFY,
            script.OP_CHECKSIG,
        ])

    def set_locktime(self, number_of_hours):
        self.locktime = datetime.utcnow() + timedelta(hours=number_of_hours)

    def generate_hash(self):
        self.secret, self.secret_hash = generate_secret_with_hash()

    def build_outputs(self):
        if not self.secret_hash:
            self.generate_hash()
            self.set_locktime(number_of_hours=self.init_hours)
        else:
            self.set_locktime(number_of_hours=self.participate_hours)

        self.build_atomic_swap_contract()

        contract_p2sh = self.contract.to_p2sh_scriptPubKey()

        self.tx_out_list = [CMutableTxOut(to_base_units(self.value), contract_p2sh), ]
        if self.utxo_value > self.value:
            change = self.utxo_value - self.value
            self.tx_out_list.append(
                CMutableTxOut(to_base_units(change), CBitcoinAddress(self.sender_address).to_scriptPubKey())
            )

    def add_fee(self):
        """Adding fee to the transaction by decreasing 'change' transaction."""
        if not self.fee:
            self.calculate_fee()
        fee_in_satoshi = to_base_units(self.fee)
        if len(self.tx.vout) == 1 or self.tx.vout[1].nValue < fee_in_satoshi:
            raise RuntimeError('Cannot subtract fee from change transaction. You need to add more input transactions.')
        self.tx.vout[1].nValue -= fee_in_satoshi

    def show_details(self):
        return {
            'contract': self.contract.hex(),
            'contract_address': str(CBitcoinAddress.from_scriptPubKey(self.contract.to_p2sh_scriptPubKey())),
            'contract_transaction': self.raw_transaction,
            'transaction_address': self.address,
            'fee': self.fee,
            'fee_per_kb': self.fee_per_kb,
            'fee_per_kb_text': f'{self.fee_per_kb:.8f} {self.symbol} / 1 kB',
            'fee_text': f'{self.fee:.8f} {self.symbol}',
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.sender_address,
            'secret': self.secret.hex() if self.secret else '',
            'secret_hash': self.secret_hash.hex(),
            'size': self.size,
            'size_text': f'{self.size} bytes',
            'value': self.value,
            'value_text': f'{self.value:.8f} {self.symbol}',
        }
