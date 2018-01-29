from datetime import datetime, timedelta
import hashlib
import struct

from bitcoin.core import COIN, CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, Hash160, b2x, lx, script, x
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

from clove.network.base import BaseNetwork


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
            script.OP_RIPEMD160,
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
            tx_in.scriptSig = script.CScript(x(outpoint['scriptPubKey']))
            self.tx_in_list.append(tx_in)

    def set_locktime(self, number_of_hours):
        self.locktime = datetime.utcnow() + timedelta(hours=number_of_hours)

    def generate_hash(self):
        self.secret = hashlib.sha256(b'some random words').digest()
        self.secret_hash = CBitcoinSecret.from_secret_bytes(self.secret)

    def build_outputs(self):
        self.generate_hash()

        self.set_locktime(number_of_hours=48)
        self.contract = self.build_atomic_swap_contract()

        self.contract_p2sh = self.contract.to_p2sh_scriptPubKey()
        self.contract_address = CBitcoinAddress.from_scriptPubKey(self.contract_p2sh)

        self.tx_out_list = [CMutableTxOut(self.value * COIN, self.contract_address), ]
        if self.outpoints_value > self.value:
            change = self.outpoints_value = self.value
            self.tx_out_list.append(CMutableTxOut(change, CBitcoinAddress(self.sender_address).to_scriptPubKey()))

    def get_secret_from_private_key(self, private_key):
        # TODO
        return secret  # noqa

    def sign(self, private_key):
        seckey = self.get_secret_from_private_key(private_key)
        for tx_in_index in range(len(self.tx.vin)):
            txin_scriptPubKey = self.tx.vin[tx_in_index].scriptSig
            sig_hash = script.SignatureHash(txin_scriptPubKey, self.tx, tx_in_index, script.SIGHASH_ALL)
            sig = seckey.sign(sig_hash) + struct.pack('<B', script.SIGHASH_ALL)
            self.tx.vin[tx_in_index].scriptSig = script.CScript([sig, seckey.pub])
            VerifyScript(
                self.tx.vin[tx_in_index].scriptSig,
                txin_scriptPubKey,
                self.tx,
                tx_in_index,
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

    def initiate_atomic_swap(self, sender_address: str, recipient_address: str, value: float, outpoints: list):
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
