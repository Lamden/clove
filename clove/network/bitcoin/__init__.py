from typing import Optional

from clove.block_explorer.insight import InsightAPIv4
from clove.network.bitcoin.base import BitcoinBaseNetwork
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class Bitcoin(InsightAPIv4, BitcoinBaseNetwork):
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
    source_code_url = 'https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp'
    api_url = 'https://insight.bitpay.com/api'
    ui_url = 'https://insight.bitpay.com'
    fee_endpoint = 'https://api.blockcypher.com/v1/btc/main'

    @classmethod
    def get_fee(cls) -> Optional[float]:
        '''Returns actual fee per kb.'''
        response = clove_req_json(cls.fee_endpoint)
        fee = response.get('high_fee_per_kb')
        if not fee:
            logger.error('Cannot find the right key (high_fee_per_kb) while getting fee in blockcypher.')
            return
        return from_base_units(fee)


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
    testnet = True
    api_url = 'https://test-insight.bitpay.com/api'
    ui_url = 'https://test-insight.bitpay.com'
    fee_endpoint = 'https://api.blockcypher.com/v1/btc/test3'
