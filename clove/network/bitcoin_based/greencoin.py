
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Greencoin(BitcoinBaseNetwork):
    """
    Class with all the necessary GRE network information based on
    http://www.github.com/greencoin-dev/GreenCoinV2/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'greencoin'
    symbols = ('GRE', )
    seeds = ()
    nodes = ('149.202.137.169', '81.83.209.224',
             '67.161.120.48', '73.12.235.88', '174.31.114.98')
    port = 11517
    message_start = b'\x05\x22\x53\x07'
    base58_prefixes = {
        'PUBKEY_ADDR': 38,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 166
    }
    source_code_url = 'http://www.github.com/greencoin-dev/GreenCoinV2/blob/master/src/chainparams.cpp'
