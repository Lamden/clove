from clove.block_explorer.insight import InsightAPIv4
from clove.network.bitcoin.base import BitcoinBaseNetwork
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class Ravencoin(InsightAPIv4, BitcoinBaseNetwork):
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
    api_url = 'https://ravencoin.network/api'
    ui_url = 'https://ravencoin.network'

    @classmethod
    def get_fee(cls) -> float:
        """Ravencoin has a different endpoint for fee (estimatesmartfee, not estimatefee)"""
        try:
            fee = clove_req_json(f'{cls.api_url}/utils/estimatesmartfee?nbBlocks=1')['1']
        except (TypeError, KeyError):
            logger.error(
                f'Incorrect response from API when getting fee from {cls.api_url}/utils/estimatefee?nbBlocks=1'
            )
            return cls._calculate_fee()
        if fee > 0:
            return fee
        logger.warning(f'({cls.symbols[0]}) Got fee = 0, calculating manually')
        return cls._calculate_fee()


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
    api_url = 'https://testnet.ravencoin.network/api'
    ui_url = 'https://testnet.ravencoin.network'
