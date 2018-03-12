from clove.network.bitcoin import Bitcoin


class TwoGIVE(Bitcoin):
    """
    Class with all the necessary  2GIVE (2GIVE) network information based on
    https://github.com/LittleDuke/2GIVE/blob/master/src/net.cpp
    (date of access: 02/19/2018)
    """
    name = '2give'
    symbols = ('2GIVE', )
    seeds = ('seed2.givecoin.io', )
    port = 6763
    message_start = b'\xce\xd5\xdb\xfa'
    base58_prefixes = {
        'PUBKEY_ADDR': 11,
        'SCRIPT_ADDR': 8,
        'SECRET_KEY': 139
    }
