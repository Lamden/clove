from clove.network.bitcoin import Bitcoin


class HealthyWormCoin(Bitcoin):
    """
    Class with all the necessary HealthyWormCoin network information based on
    https://github.com/HealthyWormDotCom/HealthyWorm/blob/master/src/net.cpp
    (date of access: 02/15/2018)
    """
    name = 'healthywormcoin'
    symbols = ('WORM', )
    seeds = ("worm.healthyworm.com", )
    port = 8064
    message_start = b'\x1c\x1b\x1c\x1d'
    base58_prefixes = {
        'PUBKEY_ADDR': 73,
        'SCRIPT_ADDR': 117,
        'SECRET_KEY': 201
    }
