from bitcoin.core import (
    CTransaction, b2x, x
)

from clove.network.base import BaseNetwork, auto_switch_params
from clove.network.bitcoin.contract import BitcoinContract
from clove.network.bitcoin.transaction import BitcoinAtomicSwapTransaction
from clove.network.bitcoin.wallet import BitcoinWallet


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
    message_start = b'\xf9\xbe\xb4\xd9'
    base58_prefixes = {
        'PUBKEY_ADDR': 0,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }

    @auto_switch_params()
    def atomic_swap(
        self,
        sender_address: str,
        recipient_address: str,
        value: float,
        solvable_utxo: list,
        secret_hash: str=None,
    ) -> BitcoinAtomicSwapTransaction:
        transaction = BitcoinAtomicSwapTransaction(
            self, sender_address, recipient_address, value, solvable_utxo, secret_hash
        )
        transaction.create_unsigned_transaction()
        return transaction

    @auto_switch_params()
    def audit_contract(self, contract: str, raw_transaction: str) -> BitcoinContract:
        return BitcoinContract(self, contract, raw_transaction)

    @classmethod
    @auto_switch_params()
    def get_wallet(cls, private_key=None, encrypted_private_key=None, password=None):
        return BitcoinWallet(private_key, encrypted_private_key, password)

    @staticmethod
    def extract_secret(raw_transaction: str) -> str:
        tx = CTransaction.deserialize(x(raw_transaction))

        if not tx.vin:
            raise ValueError('Given transaction has no inputs.')

        secret_tx_in = tx.vin[0]
        script_ops = list(secret_tx_in.scriptSig)
        if script_ops[-2] == 1:
            return b2x(script_ops[-3])

        raise ValueError('Unable to extract secret from given transaction.')


class BitcoinTestNet(Bitcoin):
    """
    Class with all the necessary BTC testing network information based on
    https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-bitcoin'
    seeds = (
        'testnet-seed.bitcoin.jonasschnelli.ch',
        # 'seed.tbtc.petertodd.org', Last check: 2018-02-21
        'seed.testnet.bitcoin.sprovoost.nl',
        'testnet-seed.bluematt.me',
    )
    port = 18333
    message_start = b'\x0b\x11\x09\x07'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
