
from clove.network.bitcoin import Bitcoin


class VeriCoin(Bitcoin):
    """
    Class with all the necessary VRC network information based on
    https://github.com/vericoin/vericoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'vericoin'
    symbols = ('VRC', )
    seeds = ('dnsseed.vericoin.info', )
    port = 58684
    message_start = b'\x70\x35\x22\x05'
    base58_prefixes = {
        'PUBKEY_ADDR': 70,
        'SCRIPT_ADDR': 132,
        'SECRET_KEY': 198
    }
