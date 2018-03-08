from clove.network.bitcoin import Bitcoin


class AsiaCoin(Bitcoin):
    """
    Class with all the necessary AsiaCoin network information based on
    https://github.com/AsiaCoin/AsiaCoinFix/blob/master/src/net.cpp
    (date of access: 02/13/2018)
    """
    name = 'asiacoin'
    symbols = ('AC', )
    seeds = ("dnsseedac.planetdollar.org", )
    port = 35656
    message_start = b'\x32\xf5\xd2\xea'
    base58_prefixes = {
        'PUBKEY_ADDR': 23,
        'SCRIPT_ADDR': 8,
        'SECRET_KEY': 151
    }

# Has no testnet
