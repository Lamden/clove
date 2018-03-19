
from clove.network.bitcoin.base import BitcoinBaseNetwork


class CannabisCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary CANN network information based on
    http://www.github.com/cannabiscoindev/cannabiscoin420/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'cannabiscoin'
    symbols = ('CANN', )
    seeds = ('seed.cannabiscoin.net', 'seed2.cannabiscoin.net', )
    port = 39348
    message_start = b'\xfe\xc3\xb9\xde'
    base58_prefixes = {
        'PUBKEY_ADDR': 28,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 156
    }
