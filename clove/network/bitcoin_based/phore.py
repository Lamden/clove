
from clove.network.bitcoin import Bitcoin


class Phore(Bitcoin):
    """
    Class with all the necessary PHR network information based on
    http://www.github.com/phoreproject/Phore/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'phore'
    symbols = ('PHR', )
    seeds = ('dns0.phore.io', 'dns1.phore.io', 'dns2.phore.io', 'dns3.phore.io', 'dns4.phore.io',
             'dns5.phore.io', 'dns6.phore.io', 'dns7.phore.io', 'dns8.phore.io', 'dns9.phore.io')
    port = 11771
    message_start = b'\x91\xc4\xfd\xe9'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 13,
        'SECRET_KEY': 212
    }
