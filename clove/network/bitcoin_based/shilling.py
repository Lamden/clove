
from clove.network.bitcoin import Bitcoin


class Shilling(Bitcoin):
    """
    Class with all the necessary SH network information based on
    http://www.github.com/yavwa/Shilling/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'shilling'
    symbols = ('SH', )
    seeds = ('wallet.cryptolife.net', 'explore.cryptolife.net',
             'seed1.cryptolife.net', 'seed2.cryptolife.net')
    port = 34621
    message_start = b'\xd8\xcf\xaa\xec'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 191
    }
