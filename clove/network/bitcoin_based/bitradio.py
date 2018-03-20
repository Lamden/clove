
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Bitradio(BitcoinBaseNetwork):
    """
    Class with all the necessary BRO network information based on
    http://www.github.com/thebitradio/Bitradio/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'bitradio'
    symbols = ('BRO', )
    seeds = ('node1.bitrad.io', 'node2.bitrad.io', 'node3.bitrad.io', )
    port = 32454
    message_start = b'\xd3\x1a\x3d\xe4'
    base58_prefixes = {
        'PUBKEY_ADDR': 26,
        'SCRIPT_ADDR': 102,
        'SECRET_KEY': 128
    }
    source_code_url = 'http://www.github.com/thebitradio/Bitradio/blob/master/src/chainparams.cpp'
