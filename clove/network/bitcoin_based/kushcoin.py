from clove.network.bitcoin import Bitcoin


class KushCoin(Bitcoin):
    """
    Class with all the necessary KushCoin network information based on
    https://github.com/kushcoin-project/kushcoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'kushcoin'
    symbols = ('KUSH', )
    seeds = ("seed-a.kushcoin.co", "seed-b.kushcoin.co", )
    port = 31544
    message_start = b'\xb4\xe9\xc2\xee'
    base58_prefixes = {
        'PUBKEY_ADDR': 45,
        'SCRIPT_ADDR': 20,
        'SECRET_KEY': 173
    }


# Has no testnet
