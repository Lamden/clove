
from clove.network.bitcoin import Bitcoin


class Riecoin(Bitcoin):
    """
    Class with all the necessary RIC network information based on
    http://www.github.com/riecoin/riecoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'riecoin'
    symbols = ('RIC', )
    seeds = ('seed.bitcoin.sipa.be', )
    port = 28333
    message_start = b'\xfc\xbc\xb2\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 60,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }
