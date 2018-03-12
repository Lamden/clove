
from clove.network.bitcoin import Bitcoin


class I0Coin(Bitcoin):
    """
    Class with all the necessary I0C network information based on
    http://www.github.com/domob1812/i0coin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'i0coin'
    symbols = ('I0C', )
    seeds = ('seed.i0coin.domob.eu', )
    port = 7333
    message_start = b'\xf1\xb2\xb3\xd4'
    base58_prefixes = {
        'PUBKEY_ADDR': 105,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }
