import base64
from datetime import datetime, timedelta
from hashlib import sha256
from random import choices
from string import ascii_letters, digits
import struct

from Crypto import Random
from Crypto.Cipher import AES
from bitcoin import SelectParams
from bitcoin.core import COIN, CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, Hash160, b2x, lx, script
from bitcoin.core.key import CPubKey
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret, P2PKHBitcoinAddress

from clove.network.base import BaseNetwork


class BitcoinWallet(object):

    def __init__(self, private_key=None, encrypted_private_key=None, password=None, testnet=False):
        if testnet:
            SelectParams('testnet')

        if private_key is None and encrypted_private_key is None:
            secret = ''.join(choices(ascii_letters + digits, k=64))
            self.secret = sha256(bytes(secret.encode('utf-8'))).digest()
            self.private_key = CBitcoinSecret.from_secret_bytes(secret=self.secret)

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

    def __init__(self, network, sender_address: str, recipient_address: str, value: float, outpoints: dict):
        self.sender_address = sender_address
        self.recipient_address = recipient_address
        self.value = value
        self.symbol = network.default_symbol

        self.tx_in_list = []
        self.tx_out_list = []
        self.outpoints = outpoints
        self.outpoints_value = 0

        self.secret = None
        self.secret_hash = None
        self.locktime = None
        self.contract = None
        self.contract_p2sh = None
        self.contract_address = None
        self.tx = None

    def build_atomic_swap_contract(self):
        self.contract = script.CScript([
            script.OP_IF,
            script.OP_SHA256,
            self.secret_hash,
            script.OP_EQUALVERIFY,
            script.OP_DUP,
            script.OP_HASH160,
            Hash160(self.recipient_address.encode()),
            script.OP_ELSE,
            str(int(self.locktime.timestamp())).encode(),
            script.OP_CHECKLOCKTIMEVERIFY,
            script.OP_DROP,
            script.OP_DUP,
            script.OP_HASH160,
            Hash160(self.sender_address.encode()),
            script.OP_ENDIF,
            script.OP_EQUALVERIFY,
            script.OP_CHECKSIG,
        ])

    def build_inputs(self):
        for outpoint in self.outpoints:
            self.outpoints_value += outpoint['value']
            tx_in = CMutableTxIn(
                COutPoint(
                    lx(outpoint['txid']),
                    outpoint['vout']
                )
            )
            tx_in.scriptSig = script.CScript.fromhex(outpoint['scriptPubKey'])
            self.tx_in_list.append(tx_in)

    def set_locktime(self, number_of_hours):
        self.locktime = datetime.utcnow() + timedelta(hours=number_of_hours)

    def generate_hash(self):
        self.secret = sha256(b'some random words').digest()
        self.secret_hash = CBitcoinSecret.from_secret_bytes(self.secret)

    def build_outputs(self):
        self.generate_hash()

        self.set_locktime(number_of_hours=48)
        self.build_atomic_swap_contract()

        self.contract_p2sh = self.contract.to_p2sh_scriptPubKey()
        self.contract_address = CBitcoinAddress.from_scriptPubKey(self.contract_p2sh)

        self.tx_out_list = [CMutableTxOut(self.value * COIN, self.contract_address), ]
        if self.outpoints_value > self.value:
            change = self.outpoints_value - self.value
            self.tx_out_list.append(CMutableTxOut(change, CBitcoinAddress(self.sender_address).to_scriptPubKey()))

    def sign(self, wallet: BitcoinWallet):
        for tx_index, tx_in in enumerate(self.tx.vin):
            original_script_signature = tx_in.scriptSig
            sig_hash = script.SignatureHash(original_script_signature, self.tx, tx_index, script.SIGHASH_ALL)
            sig = wallet.private_key.sign(sig_hash) + struct.pack('<B', script.SIGHASH_ALL)
            tx_in.scriptSig = script.CScript([sig, wallet.private_key.pub])
            VerifyScript(
                tx_in.scriptSig,
                original_script_signature,
                self.tx,
                tx_index,
                (SCRIPT_VERIFY_P2SH,)
            )

    def create_unsign_transaction(self):
        self.build_inputs()
        assert self.outpoints_value >= self.value
        self.build_outputs()
        self.tx = CMutableTransaction(self.tx_in_list, self.tx_out_list)

    def publish(self):
        pass

    def __dict__(self):
        return {
            'contract': self.contract.hex(),
            'contract_address': str(self.contract_address),
            'contract_transaction': b2x(self.tx.serialize()),
            'contract_transaction_hash': self.tx.GetHash().hex(),
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.sender_address,
            # 'refund_transaction': '',
            # 'refund_transaction_hash': '',
            'secret': self.secret.hex(),
            'secret_hash': self.secret_hash.hex(),
            'value': self.value,
            'value_text': f'{self.value} {self.symbol}',
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
        outpoints: list
    ) -> BitcoinTransaction:
        transaction = BitcoinTransaction(self, sender_address, recipient_address, value, outpoints)
        transaction.create_unsign_transaction()
        return transaction


class TestNetBitcoin(Bitcoin):
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
