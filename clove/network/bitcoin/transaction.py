from datetime import datetime, timedelta
import struct

from bitcoin.core import CMutableTransaction, CMutableTxOut, b2lx, b2x, script, x
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress

from clove.constants import TRANSACTION_BROADCASTING_MAX_ATTEMPTS
from clove.network.base import auto_switch_params
from clove.network.bitcoin.wallet import BitcoinWallet
from clove.utils.bitcoin import btc_to_satoshi
from clove.utils.hashing import generate_secret_with_hash
from clove.utils.logging import logger


class BitcoinTransaction(object):

    @auto_switch_params(1)
    def __init__(self, network, recipient_address: str, value: float, solvable_utxo: list, tx_locktime: int=0):
        self.recipient_address = recipient_address
        self.value = value
        self.network = network
        self.symbol = network.default_symbol

        self.solvable_utxo = solvable_utxo
        self.utxo_value = sum(utxo.value for utxo in self.solvable_utxo)
        self.tx_in_list = [utxo.tx_in for utxo in self.solvable_utxo]
        self.tx_out_list = []

        self.tx = None
        self.tx_locktime = tx_locktime
        self.fee = 0.0
        self.fee_per_kb = 0.0

    def build_outputs(self):
        self.tx_out_list = [
            CMutableTxOut(btc_to_satoshi(self.value), CBitcoinAddress(self.recipient_address).to_scriptPubKey())
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
        for attempt in range(1, TRANSACTION_BROADCASTING_MAX_ATTEMPTS + 1):
            transaction_hash = self.network.broadcast_transaction(self.tx)

            if transaction_hash is None:
                logger.warning('Transaction broadcast attempt no. %s failed. Retrying...', attempt)
                continue

            logger.info('Transaction broadcast is successful. End of broadcasting process.')
            return transaction_hash

        logger.warning(
            '%s attempts to broadcast transaction failed. Broadcasting process terminates!',
            TRANSACTION_BROADCASTING_MAX_ATTEMPTS
        )

    @property
    def size(self) -> int:
        """Returns the size of a transaction represented in bytes."""
        return len(self.tx.serialize())

    def calculate_fee(self):
        """Calculating fee for given transaction based on transaction size and estimated fee per kb."""
        if not self.fee_per_kb:
            self.fee_per_kb = self.network.get_current_fee_per_kb()
        self.fee = round((self.fee_per_kb / 1000) * self.size, 8)

    def add_fee(self):
        """Adding fee to the transaction by decreasing 'change' transaction."""
        if not self.fee:
            self.calculate_fee()
        fee_in_satoshi = btc_to_satoshi(self.fee)
        if self.tx.vout[0].nValue < fee_in_satoshi:
            raise RuntimeError('Cannot subtract fee from transaction. You need to add more input transactions.')
        self.tx.vout[0].nValue -= fee_in_satoshi

    def show_details(self):
        return {
            'transaction': b2x(self.tx.serialize()),
            'transaction_hash': b2lx(self.tx.GetHash()),
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
        super().__init__(network, recipient_address, value, solvable_utxo, tx_locktime)
        self.sender_address = sender_address
        self.secret = None
        self.secret_hash = x(secret_hash) if secret_hash else None
        self.locktime = None
        self.contract = None

    def build_atomic_swap_contract(self):
        self.contract = script.CScript([
            script.OP_IF,
            script.OP_SHA256,
            self.secret_hash,
            script.OP_EQUALVERIFY,
            script.OP_DUP,
            script.OP_HASH160,
            CBitcoinAddress(self.recipient_address),
            script.OP_ELSE,
            int(self.locktime.timestamp()),
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

        self.tx_out_list = [CMutableTxOut(btc_to_satoshi(self.value), contract_p2sh), ]
        if self.utxo_value > self.value:
            change = self.utxo_value - self.value
            self.tx_out_list.append(
                CMutableTxOut(btc_to_satoshi(change), CBitcoinAddress(self.sender_address).to_scriptPubKey())
            )

    def add_fee(self):
        """Adding fee to the transaction by decreasing 'change' transaction."""
        if not self.fee:
            self.calculate_fee()
        fee_in_satoshi = btc_to_satoshi(self.fee)
        if len(self.tx.vout) == 1 or self.tx.vout[1].nValue < fee_in_satoshi:
            raise RuntimeError('Cannot subtract fee from change transaction. You need to add more input transactions.')
        self.tx.vout[1].nValue -= fee_in_satoshi

    def show_details(self):
        return {
            'contract': self.contract.hex(),
            'contract_transaction': b2x(self.tx.serialize()),
            'transaction_hash': b2lx(self.tx.GetHash()),
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
