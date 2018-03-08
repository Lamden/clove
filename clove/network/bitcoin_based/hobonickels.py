from clove.network.bitcoin import Bitcoin


class HoboNickels(Bitcoin):
    """
    Class with all the necessary HoboNickels network information based on
    https://github.com/crypto-expert/hobonickels/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'hobonickels'
    symbols = ('HBN', )
    seeds = ("seed.scrypt.io", "seed.hobonickels.info", "seed2.hobonickels.info",
             "seed3.hobonickels.info", "seed4.hobonickels.info", "hbn.altcointech.net")
    port = 7372
    message_start = b'\xe4\xe8\xe9\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 34,
        'SCRIPT_ADDR': 8,
        'SECRET_KEY': 162
    }


# Has no Testnet
