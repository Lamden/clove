
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Rubycoin(BitcoinBaseNetwork):
    """
    Class with all the necessary RBY network information based on
    http://www.github.com/rubycoinorg/rubycoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'rubycoin'
    symbols = ('RBY', )
    seeds = ('neptune.rubycoin.org', 'pluto.rubycoin.org', )
    port = 5937
    message_start = b'\x13\x12\x16\x11'
    base58_prefixes = {
        'PUBKEY_ADDR': 60,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 188
    }
    source_code_url = 'http://www.github.com/rubycoinorg/rubycoin/blob/master/src/chainparams.cpp'
