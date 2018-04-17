import json
from typing import Optional

from bitcoin.core import COIN

from clove.network.bitcoin.base import BitcoinBaseNetwork
from clove.utils.external_source import clove_req
from clove.utils.logging import logger


class Ravencoin(BitcoinBaseNetwork):
    """
    Class with all the necessary RVN network information based on
    https://github.com/RavenProject/Ravencoin/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'raven'
    symbols = ('RVN', )
    seeds = (
        "seed-raven.ravencoin.org",
        "seed-raven.bitactivate.com"
    )
    port = 8767
    message_start = b'\x52\x41\x56\x4e'
    base58_prefixes = {
        'PUBKEY_ADDR': 60,
        'SCRIPT_ADDR': 122,
        'SECRET_KEY': 128
    }
    source_code_url = 'https://github.com/RavenProject/Ravencoin/blob/master/src/chainparams.cpp'

    @classmethod
    def get_current_fee_per_kb(cls) -> Optional[float]:

        fees = []

        # getting last transactions
        number_of_transactions = 10
        older_than_minutes = 60
        resp = clove_req(f'http://threeeyed.info/ext/getlasttxs/{number_of_transactions}/{older_than_minutes}')
        if not resp or resp.status != 200:
            return
        try:
            last_transactions = json.loads(resp.read().decode())['data'][:10]
        except KeyError:
            logger.error('This is not a valid JSON format')
            return

        for tx in last_transactions:

            # getting size
            resp = clove_req(f'http://threeeyed.info/api/getrawtransaction?txid={tx["txid"]}&decrypt=1')
            if not resp or resp.status != 200:
                continue
            try:
                size = json.loads(resp.read().decode())['size']
            except KeyError:
                logger.error('This is not a valid JSON format')
                continue

            total_vin = sum([vin['amount'] for vin in tx['vin']])
            total_vout = tx['total']
            fee = total_vin - total_vout
            tx_fee_per_kb = ((fee * 1000) / size) / COIN

            logger.debug('Calculated fee per kb as %s for tx %s', tx_fee_per_kb, tx["txid"])

            if tx_fee_per_kb > 0:
                fees.append(tx_fee_per_kb)

        return round(sum(fees) / len(fees), 8) if fees else None


class RavencoinTestNet(Ravencoin):
    """
    Class with all the necessary RVN testing network information based on
    https://github.com/RavenProject/Ravencoin/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'test-raven'
    seeds = (
        "seed-testnet-raven.ravencoin.org",
        "seed-testnet-raven.bitactivate.com"
    )
    port = 18767
    message_start = b'\x52\x56\x4E\x54'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True

    @classmethod
    def get_current_fee_per_kb(cls) -> Optional[float]:
        raise NotImplementedError
