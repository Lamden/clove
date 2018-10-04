from typing import Optional

from clove.block_explorer.insight import InsightAPIv4
from clove.network.bitcoin.base import BitcoinBaseNetwork, NoAPI
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class Dash(InsightAPIv4, BitcoinBaseNetwork):
    """
    Class with all the necessary DASH network information based on
    https://github.com/dashpay/dash/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'dash'
    symbols = ('DASH', )
    seeds = (
        'dnsseed.dash.org',
        'dnsseed.dashdot.io',
        'dnsseed.masternode.io',
        # 'dnsseed.dashpay.io', Last check: 2018-02-21
    )
    port = 9999
    message_start = b'\xbf\x0c\x6b\xbd'
    base58_prefixes = {
        'PUBKEY_ADDR': 76,
        'SCRIPT_ADDR': 16,
        'SECRET_KEY': 204
    }
    source_code_url = 'https://github.com/dashpay/dash/blob/master/src/chainparams.cpp'
    api_url = 'https://insight.dash.org/insight-api'
    ui_url = 'https://insight.dash.org/insight'

    @classmethod
    def get_fee(cls) -> Optional[float]:
        '''Returns actual fee per kb.'''
        response = clove_req_json('https://api.blockcypher.com/v1/dash/main')
        fee = response.get('high_fee_per_kb')
        if not fee:
            logger.error('Cannot find the right key (high_fee_per_kb) while getting fee in blockcypher.')
            return
        return from_base_units(fee)


class DashTestNet(NoAPI, Dash):
    """
    Class with all the necessary DASH testing network information based on
    https://github.com/dashpay/dash/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-dash'
    seeds = (
        # 'testnet-seed.dashdot.io', Last check: 2018-02-21
        'test.dnsseed.masternode.io',
    )
    port = 19999
    message_start = b'\xce\xe2\xca\xff'
    base58_prefixes = {
        'PUBKEY_ADDR': 140,
        'SCRIPT_ADDR': 19,
        'SECRET_KEY': 239
    }
    testnet = True
