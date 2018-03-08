
from clove.network.bitcoin import Bitcoin


class Pandacoin(Bitcoin):
    """
    Class with all the necessary PND network information based on
    http://www.github.com/DigitalPandacoin/pandacoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'pandacoin'
    symbols = ('PND', )
    seeds = ('server1.cryptodepot.org', )
    port = 22445
    message_start = b'\xc0\xc0\xc0\xc0'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 22,
        'SECRET_KEY': 183
    }
