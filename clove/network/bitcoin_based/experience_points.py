from clove.network.bitcoin import Bitcoin


class ExperiencePoints(Bitcoin):
    """
    Class with all the necessary Experience Points XP network information based on
    https://github.com/eXperiencePoints/XPCoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'experiencepoints'
    symbols = ('XP', )
    seeds = ('seed1.xpcoin.io', 'seed2.xpcoin.io',
             'seed3.xpcoin.io', 'seed4.xpcoin.io')
    port = 28192
    message_start = b'\xb4\xf8\xe2\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 75,
        'SCRIPT_ADDR': 20,
        'SECRET_KEY': 203
    }
