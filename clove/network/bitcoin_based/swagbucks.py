
from clove.network.bitcoin.base import BitcoinBaseNetwork


class SwagBucks(BitcoinBaseNetwork):
    """
    Class with all the necessary BUCKS network information based on
    http://www.github.com/pinkmagicdev/SwagBucks/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'swagbucks'
    symbols = ('BUCKS', )
    seeds = ('seed.swagsociety.me', )
    port = 1337
    message_start = b'\x70\x35\x22\x05'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 125,
        'SECRET_KEY': 153
    }
    source_code_url = 'http://www.github.com/pinkmagicdev/SwagBucks/blob/master/src/chainparams.cpp'
