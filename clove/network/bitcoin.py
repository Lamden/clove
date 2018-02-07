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
from bitcoin.core import COIN, CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, b2x, lx, script
from bitcoin.core.key import CPubKey
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

from clove.network.base import BaseNetwork
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


class BitcoinTransaction(object):

    def __init__(self, network, sender_address: str, recipient_address: str, value: float, solvable_utxo: dict):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.value = value
        self.network = network
        self.symbol = network.default_symbol

        self.tx_in_list = []
        self.tx_out_list = []
        self.solvable_utxo = solvable_utxo
        self.utxo_value = 0

        self.secret = None
        self.secret_hash = None
        self.locktime = None
        self.contract = None
        self.tx = None
        self.fee = None
        self.fee_per_kb = None

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
            str(int(self.locktime.timestamp())).encode(),
            script.OP_CHECKLOCKTIMEVERIFY,
            script.OP_DROP,
            script.OP_DUP,
            script.OP_HASH160,
            CBitcoinAddress(self.sender_address),
            script.OP_ENDIF,
            script.OP_EQUALVERIFY,
            script.OP_CHECKSIG,
        ])

    def build_inputs(self):
        for utxo in self.solvable_utxo:
            self.utxo_value += utxo['value']
            tx_in = CMutableTxIn(
                COutPoint(
                    lx(utxo['txid']),
                    utxo['vout']
                )
            )
            self.tx_in_list.append(tx_in)

    def set_locktime(self, number_of_hours):
        self.locktime = datetime.utcnow() + timedelta(hours=number_of_hours)

    def generate_hash(self):
        self.secret, self.secret_hash = generate_secret_with_hash()

    def build_outputs(self):
        self.generate_hash()

        self.set_locktime(number_of_hours=48)
        self.build_atomic_swap_contract()

        self.tx_out_list = [CMutableTxOut(self.value * COIN, self.contract), ]
        if self.utxo_value > self.value:
            change = self.utxo_value - self.value
            self.tx_out_list.append(
                CMutableTxOut(change * COIN, CBitcoinAddress(self.sender_address).to_scriptPubKey())
            )

    def add_fee_and_sign(self, wallet):
        """Signing transaction and adding fee under the hood."""

        # signing the transaction for the first time to get the right transaction size
        self.sign(wallet)

        # adding fee based on transaction size (this will modify the transaction)
        self.add_fee()

        # signing the modified transaction
        self.sign(wallet)

    def sign(self, wallet: BitcoinWallet):
        """Signing transaction using the wallet object."""

        for tx_index, tx_in in enumerate(self.tx.vin):

            tx_script = script.CScript.fromhex(self.solvable_utxo[tx_index]['script'])
            sig_hash = script.SignatureHash(tx_script, self.tx, tx_index, script.SIGHASH_ALL)
            sig = wallet.private_key.sign(sig_hash) + struct.pack('<B', script.SIGHASH_ALL)
            tx_in.scriptSig = script.CScript([sig, wallet.private_key.pub])

            VerifyScript(
                tx_in.scriptSig,
                tx_script,
                self.tx,
                tx_index,
                (SCRIPT_VERIFY_P2SH,)
            )

    def create_unsign_transaction(self):
        self.build_inputs()
        assert self.utxo_value >= self.value
        self.build_outputs()
        self.tx = CMutableTransaction(self.tx_in_list, self.tx_out_list)

    def publish(self):
        pass

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
        if len(self.tx.vout) == 1 or self.tx.vout[1].nValue < self.fee:
            raise RuntimeError('Cannot subtract fee from change transaction. You need to add more input transactions.')
        fee_in_satoshi = round(self.fee * COIN)
        self.tx.vout[1].nValue -= fee_in_satoshi

    def show_details(self):
        return {
            'contract': self.contract.hex(),
            'contract_transaction': b2x(self.tx.serialize()),
            'contract_transaction_hash': self.tx.GetHash().hex(),
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
    ) -> BitcoinTransaction:
        transaction = BitcoinTransaction(self, sender_address, recipient_address, value, solvable_utxo)
        transaction.create_unsign_transaction()
        return transaction

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
                return data['high_fee_per_kb'] / COIN
        except (URLError, HTTPError):
            return
