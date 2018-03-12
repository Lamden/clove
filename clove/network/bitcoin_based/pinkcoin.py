from clove.network.bitcoin import Bitcoin


class Pinkcoin(Bitcoin):
    """
    Class with all the necessary Pinkcoin network information based on
    https://github.com/pinkdev/pink2/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'pinkcoin'
    symbols = ('PINK', )
    seeds = ("pinkarmy.ml",
             "frankfurt.pinkarmy.ml",
             "paris.pinkarmy.ml",
             "singapore.pinkarmy.ml",
             "sydney.pinkarmy.ml",
             "tokyo.pinkarmy.ml")
    port = 9134
    message_start = b'\xf2\xf4\xf9\xfb'
    base58_prefixes = {
        'PUBKEY_ADDR': 3,
        'SCRIPT_ADDR': 28,
        'SECRET_KEY': 131
    }


# Has no testnet
