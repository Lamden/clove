from clove.network.bitcoin import Bitcoin


class Equitrade(Bitcoin):
    """
    Class with all the necessary Equitrade network information based on
    https://github.com/equitrader/equitrade/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'equitrade'
    symbols = ('EQT', )
    seeds = ("seed1.cryptolife.net", "seed2.cryptolife.net", "seed3.cryptolife.net",
             "seed5.cryptolife.net", "wallet.cryptolife.net", "explore.cryptolife.net")
    port = 43103
    message_start = b'\xb4\xf8\xe7\xa5'
    base58_prefixes = {
        'PUBKEY_ADDR': 33,
        'SCRIPT_ADDR': 20,
        'SECRET_KEY': 161
    }


# Equitrade has no Testnet
