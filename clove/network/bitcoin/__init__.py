import os
from typing import Optional

from bitcoin.core import b2x, script

from clove.network.base import BaseNetwork, auto_switch_params
from clove.network.bitcoin.contract import BitcoinContract
from clove.network.bitcoin.transaction import BitcoinAtomicSwapTransaction
from clove.network.bitcoin.wallet import BitcoinWallet
from clove.utils.bitcoin import deserialize_raw_transaction
from clove.utils.external_source import extract_scriptsig_from_redeem_transaction
from clove.utils.logging import logger


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
    def extract_secret(raw_transaction: str=None, scriptsig: str=None) -> str:

        if not raw_transaction and not scriptsig:
            raise ValueError('raw_transaction or scriptsig have to be provided.')

        if raw_transaction:
            tx = deserialize_raw_transaction(raw_transaction)

            if not tx.vin:
                raise ValueError('Given transaction has no inputs.')

            secret_tx_in = tx.vin[0]
            script_ops = list(secret_tx_in.scriptSig)
        else:
            script_ops = list(script.CScript.fromhex(scriptsig))

        if script_ops[-2] == 1:
            return b2x(script_ops[-3])

        raise ValueError('Unable to extract secret.')

    @classmethod
    def extract_secret_from_redeem_transaction(cls, contract_address: str) -> Optional[str]:

        if cls.is_test_network() and cls.name != 'test-bitcoin':
            raise NotImplementedError

        try:
            scriptsig = extract_scriptsig_from_redeem_transaction(
                network=cls.symbols[0],
                contract_address=contract_address,
                testnet=cls.is_test_network(),
                cryptoid_api_key=os.getenv('CRYPTOID_API_KEY'),
            )
        except NotImplementedError:
            logger.debug('%s: network is not supported', cls.name)
            return
        except ValueError as e:
            logger.debug(e)
            return

        if scriptsig:
            try:
                return cls.extract_secret(scriptsig)
            except ValueError as e:
                logger.debug(e)
                return


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
