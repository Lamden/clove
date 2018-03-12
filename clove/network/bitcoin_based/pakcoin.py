
from clove.network.bitcoin import Bitcoin


class Pakcoin(Bitcoin):
    """
    Class with all the necessary PAK network information based on
    http://www.github.com/pakcoin-project/pakcoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'pakcoin'
    symbols = ('PAK', )
    seeds = ('seed.pakcoin.org', )
    port = 7867
    message_start = b'\x70\x61\x6b\x63'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 183
    }
