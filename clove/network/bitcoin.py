import base64
from datetime import datetime, timedelta
from hashlib import sha256
import json
import struct
import sys
from urllib.error import HTTPError, URLError
import urllib.request

from Crypto import Random
from Crypto.Cipher import AES
from bitcoin import SelectParams
from bitcoin.core import (
    CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, CTransaction, b2lx, b2x, lx, script, x
)
from bitcoin.core.key import CPubKey
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

from clove.network.base import BaseNetwork
from clove.utils.bitcoin import btc_to_satoshi, satoshi_to_btc
from clove.utils.hashing import generate_secret_with_hash


class BitcoinWallet(object):

    def __init__(self, private_key=None, encrypted_private_key=None, password=None, testnet=False):
        if testnet:
            SelectParams('testnet')

        if private_key is None and encrypted_private_key is None:
            _, secret_hash = generate_secret_with_hash()
            self.private_key = CBitcoinSecret.from_secret_bytes(secret=secret_hash)

        elif private_key is not None:
            self.private_key = CBitcoinSecret(private_key)

        elif encrypted_private_key is not None and password is not None:
            self.private_key = CBitcoinSecret(self.decrypt_private_key(encrypted_private_key, password))

        elif password is None:
            raise TypeError(
                "__init__() missing 'password' argument, since 'encrypted_private_key' argument was provided"
            )

        self.public_key = self.private_key.pub

    def get_private_key(self) -> str:
        return str(self.private_key)

    def get_public_key(self) -> CPubKey:
        return self.public_key

    def get_address(self) -> str:
        return str(P2PKHBitcoinAddress.from_pubkey(self.public_key))

    @staticmethod
    def encrypt_private_key(private_key: str, password: str) -> bytes:
        """Encrypt private key with the password."""
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(sha256(bytes(password.encode('utf-8'))).digest(), AES.MODE_CFB, iv)
        encrypted_private_key = base64.b64encode(iv + cipher.encrypt(private_key))
        return encrypted_private_key

    @staticmethod
    def decrypt_private_key(encrypted_private_key: bytes, password: str) -> str:
        """Decrypt private key with the password."""
        encrypted_private_key = base64.b64decode(encrypted_private_key)
        iv = encrypted_private_key[:AES.block_size]
        cipher = AES.new(sha256(bytes(password.encode('utf-8'))).digest(), AES.MODE_CFB, iv)
        private_key = cipher.decrypt(encrypted_private_key[AES.block_size:])
        return str(private_key, 'ascii')


class Utxo(object):

    def __init__(self, tx_id, vout, value, tx_script, wallet=None, secret=None, refund=False):
        self.tx_id = tx_id
        self.vout = vout
        self.value = value
        self.tx_script = tx_script
        self.wallet = wallet
        self.secret = secret
        self.refund = refund

    @property
    def outpoint(self):
        return COutPoint(lx(self.tx_id), self.vout)

    @property
    def tx_in(self):
        return CMutableTxIn(self.outpoint, scriptSig=script.CScript(self.unsigned_script_sig), nSequence=0)

    @property
    def parsed_script(self):
        return script.CScript.fromhex(self.tx_script)

    @property
    def unsigned_script_sig(self):
        if self.refund:
            return [script.OP_FALSE]
        elif self.secret:
            return [x(self.secret), script.OP_TRUE]
        else:
            return []

    def __repr__(self):
        return "Utxo(tx_id='{}', vout='{}', value='{}', tx_script='{}', wallet={}, secret={}, refund={})".format(
            self.tx_id,
            self.vout,
            self.value,
            self.tx_script,
            self.wallet,
            str(self.secret),
            self.refund,
        )


class BitcoinTransaction(object):

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

    def sign(self, default_wallet: BitcoinWallet=None):
        """Signing transaction using the wallet object."""

        for tx_index, tx_in in enumerate(self.tx.vin):
            utxo = self.solvable_utxo[tx_index]
            wallet = utxo.wallet or default_wallet

            if wallet is None:
                raise RuntimeError('Cannot sign transaction without a wallet.')

            tx_script = utxo.parsed_script
            sig_hash = script.SignatureHash(tx_script, self.tx, tx_index, script.SIGHASH_ALL)
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
        return self.network.broadcast_transaction(self.tx)

    @property
    def size(self) -> int:
        """Returns the size of a transaction represented in byte."""
        return sys.getsizeof(self.tx.serialize())

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


class BitcoinInitTransaction(BitcoinTransaction):

    def __init__(
        self,
        network,
        sender_address: str,
        recipient_address: str,
        value: float,
        solvable_utxo: list,
        tx_locktime: int=0
    ):
        super().__init__(network, recipient_address, value, solvable_utxo, tx_locktime)
        self.sender_address = sender_address
        self.secret = None
        self.secret_hash = None
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
        self.generate_hash()

        self.set_locktime(number_of_hours=48)
        self.build_atomic_swap_contract()

        self.tx_out_list = [CMutableTxOut(btc_to_satoshi(self.value), self.contract), ]
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
            'secret': self.secret.hex(),
            'secret_hash': self.secret_hash.hex(),
            'size': self.size,
            'size_text': f'{self.size} bytes',
            'value': self.value,
            'value_text': f'{self.value:.8f} {self.symbol}',
        }


class BitcoinContract(object):

    def __init__(self, network, raw_transaction: str):
        self.network = network
        self.symbol = self.network.default_symbol
        self.tx = CTransaction.deserialize(x(raw_transaction))

        if not self.tx.vout:
            raise ValueError('Given transaction has no outputs.')

        contract_tx_out = self.tx.vout[0]
        script_ops = list(contract_tx_out.scriptPubKey)
        if self.is_valid_contract_script(script_ops):
            self.recipient_address = str(P2PKHBitcoinAddress.from_bytes(script_ops[6]))
            self.refund_address = str(P2PKHBitcoinAddress.from_bytes(script_ops[13]))
            self.locktime_timestamp = int.from_bytes(script_ops[8], byteorder='little')
            self.locktime = datetime.fromtimestamp(self.locktime_timestamp)
            self.secret_hash = b2x(script_ops[2])
            self.value = satoshi_to_btc(contract_tx_out.nValue)
        else:
            raise ValueError('Given transaction is not a valid contract.')

    @property
    def transaction_hash(self):
        return b2lx(self.tx.GetHash())

    @staticmethod
    def is_valid_contract_script(script_ops):
        try:
            is_valid = (
                script_ops[0] == script.OP_IF
                and script_ops[1] == script.OP_SHA256
                and script_ops[3] == script_ops[15] == script.OP_EQUALVERIFY
                and script_ops[4] == script_ops[11] == script.OP_DUP
                and script_ops[5] == script_ops[12] == script.OP_HASH160
                and script_ops[7] == script.OP_ELSE
                and script_ops[9] == script.OP_CHECKLOCKTIMEVERIFY
                and script_ops[10] == script.OP_DROP
                and script_ops[14] == script.OP_ENDIF
                and script_ops[16] == script.OP_CHECKSIG
            )
        except IndexError:
            is_valid = False

        return is_valid

    def get_contract_utxo(self, wallet=None, secret=None, refund=False):
        return Utxo(
            tx_id=self.transaction_hash,
            vout=0,
            value=self.value,
            tx_script=self.tx.vout[0].scriptPubKey.hex(),
            wallet=wallet,
            secret=secret,
            refund=refund
        )

    def redeem(self, wallet, secret):
        transaction = BitcoinTransaction(
            network=self.network,
            recipient_address=self.recipient_address,
            value=self.value,
            solvable_utxo=[self.get_contract_utxo(wallet, secret)]
        )
        transaction.create_unsigned_transaction()
        return transaction

    def refund(self, wallet):
        transaction = BitcoinTransaction(
            network=self.network,
            recipient_address=self.refund_address,
            value=self.value,
            solvable_utxo=[self.get_contract_utxo(wallet, refund=True)],
            tx_locktime=self.locktime_timestamp,
        )
        transaction.create_unsigned_transaction()
        return transaction

    def show_details(self):
        return {
            'transaction_hash': self.transaction_hash,
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.refund_address,
            'secret_hash': self.secret_hash,
            'value': self.value,
            'value_text': f'{self.value:.8f} {self.symbol}',
        }


class Bitcoin(BaseNetwork):
    """
    Class with all the necessary BTC network information based on
    https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'bitcoin'
    symbols = ('BTC', 'XBT')
    seeds = (
        'seed.bitcoin.sipa.be',
        'dnsseed.bluematt.me',
        'dnsseed.bitcoin.dashjr.org',
        'seed.bitcoinstats.com',
        'seed.bitcoin.jonasschnelli.ch',
        'seed.btc.petertodd.org',
    )
    port = 8333

    def __init__(self):
        SelectParams('mainnet')

    def initiate_atomic_swap(
        self,
        sender_address: str,
        recipient_address: str,
        value: float,
        solvable_utxo: list
    ) -> BitcoinInitTransaction:
        transaction = BitcoinInitTransaction(self, sender_address, recipient_address, value, solvable_utxo)
        transaction.create_unsigned_transaction()
        return transaction

    def audit_contract(self, raw_transaction: str) -> BitcoinContract:
        return BitcoinContract(self, raw_transaction)

    @staticmethod
    def get_wallet(private_key=None, encrypted_private_key=None, password=None):
        return BitcoinWallet(private_key, encrypted_private_key, password)


class BitcoinTestNet(Bitcoin):
    """
    Class with all the necessary BTC testing network information based on
    https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-bitcoin'
    seeds = (
        'testnet-seed.bitcoin.jonasschnelli.ch',
        'seed.tbtc.petertodd.org',
        'seed.testnet.bitcoin.sprovoost.nl',
        'testnet-seed.bluematt.me',
    )
    port = 18333

    def __init__(self):
        SelectParams('testnet')

    @staticmethod
    def get_wallet(private_key=None, encrypted_private_key=None, password=None):
        return BitcoinWallet(private_key, encrypted_private_key, password, testnet=True)

    @classmethod
    def get_current_fee_per_kb(cls) -> float:
        """Returns current high priority (1-2 blocks) fee estimates."""
        try:
            with urllib.request.urlopen('https://api.blockcypher.com/v1/btc/test3') as url:
                if url.status != 200:
                    return
                data = json.loads(url.read().decode())
                return satoshi_to_btc(data['high_fee_per_kb'])
        except (URLError, HTTPError):
            return
