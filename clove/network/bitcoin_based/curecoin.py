from clove.network.bitcoin import Bitcoin


class Curecoin(Bitcoin):
    """
    Class with all the necessary Curecoin network information based on
    https://github.com/cygnusxi/curecoinsource/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'curecoin'
    symbols = ('CURE', )
    seeds = ("seed.curecoin.net", "seed2.curecoin.net", )
    port = 9911
    message_start = b'\xe4\xe8\xe9\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 25,
        'SCRIPT_ADDR': 30,
        'SECRET_KEY': 253
    }


# Has no Testnet
