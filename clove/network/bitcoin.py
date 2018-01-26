from datetime import datetime, timedelta
import hashlib
import struct

from bitcoin.core import COIN, CMutableTransaction, CMutableTxIn, CMutableTxOut, COutPoint, Hash160, b2x, lx, script, x
from bitcoin.core.scripteval import SCRIPT_VERIFY_P2SH, VerifyScript
from bitcoin.wallet import CBitcoinAddress, CBitcoinSecret

from clove.network.base import BaseNetwork


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

    @staticmethod
    def atomic_swap_contract(
        sender_address: str,
        recipient_address: str,
        secret_hash: str,
        locktime: datetime,
    ):
        return script.CScript([
            script.OP_IF,
            script.OP_RIPEMD160,
            secret_hash,
            script.OP_EQUALVERIFY,
            script.OP_DUP,
            script.OP_HASH160,
            Hash160(recipient_address.encode()),
            script.OP_ELSE,
            str(int(locktime.timestamp())).encode(),
            script.OP_CHECKLOCKTIMEVERIFY,
            script.OP_DROP,
            script.OP_DUP,
            script.OP_HASH160,
            Hash160(sender_address.encode()),
            script.OP_ENDIF,
        ])

    @staticmethod
    def build_inputs(outpoints):
        tx_in_list = []
        total_value = 0

        for outpoint in outpoints:
            total_value += outpoint['value']
            tx_in = CMutableTxIn(
                COutPoint(
                    lx(outpoint['txid']),
                    outpoint['vout']
                )
            )
            tx_in.scriptSig = script.CScript(x(outpoint['scriptPubKey']))
            tx_in_list.append(tx_in)

        return tx_in_list, total_value

    @classmethod
    def build_outputs(cls, sender_address: str, recipient_address: str, value: float):
        secret = hashlib.sha256(b'some random words').digest()
        secret_hash = CBitcoinSecret.from_secret_bytes(secret)

        locktime = datetime.utcnow() + timedelta(hours=48)
        contract = cls.atomic_swap_contract(
            sender_address,
            recipient_address,
            secret_hash,
            locktime,
        )

        contract_p2sh = contract.to_p2sh_scriptPubKey()
        contract_address = CBitcoinAddress.from_scriptPubKey(contract_p2sh)
        tx_out_list = [CMutableTxOut(value * COIN, contract_address), ]
        return tx_out_list, secret, secret_hash, locktime, contract, contract_address

    @staticmethod
    def get_secret_from_private_key(private_key):
        # TODO
        return secret  # noqa

    @classmethod
    def sign_transaction(cls, tx, private_key):
        seckey = cls.get_secret_from_private_key(private_key)
        for tx_in_index in range(len(tx.vin)):
            txin_scriptPubKey = tx.vin[tx_in_index].scriptSig
            sig_hash = script.SignatureHash(txin_scriptPubKey, tx, tx_in_index, script.SIGHASH_ALL)
            sig = seckey.sign(sig_hash) + struct.pack('<B', script.SIGHASH_ALL)
            tx.vin[tx_in_index].scriptSig = script.CScript([sig, seckey.pub])
            VerifyScript(tx.vin[tx_in_index].scriptSig, txin_scriptPubKey, tx, tx_in_index, (SCRIPT_VERIFY_P2SH,))
        return tx

    def initiate_atomic_swap(
        self,
        sender_address: str,
        recipient_address: str,
        value: float,
        outpoints: list,
        private_key: str,
    ):

        tx_in_list, outpoints_value = self.build_inputs(outpoints)
        assert outpoints_value >= value

        tx_out_list, secret, secret_hash, locktime, contract, contract_address = self.build_outputs(
            sender_address,
            recipient_address,
            value,
        )

        unsigned_tx = CMutableTransaction(tx_in_list, tx_out_list)
        signed_tx = self.sign_transaction(unsigned_tx, private_key)

        return self.dict_to_namedtuple({
            'contract': contract.hex(),
            'contract_address': str(contract_address),
            'contract_transaction': b2x(signed_tx.serialize()),
            'contract_transaction_hash': signed_tx.GetHash().hex(),
            'locktime': locktime,
            'recipient_address': recipient_address,
            'refund_address': sender_address,
            # 'refund_transaction': '',
            # 'refund_transaction_hash': '',
            'secret': secret.hex(),
            'secret_hash': secret_hash.hex(),
            'value': value,
            'value_text': f'{value} {self.default_symbol}',
        })


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
