from clove.network.bitcoin import Bitcoin


class Eryllium(Bitcoin):
    """
    Class with all the necessary Eryllium (ERY) network information based on
    https://github.com/Eryllium/project/blob/master/src/net.cpp
    (date of access: 02/16/2018)
    """
    name = 'eryllium'
    symbols = ('ERY', )
    seeds = ('seed1.cryptolife.net', 'seed2.cryptolife.net',
             'seed3.cryptolife.net', 'electrum1.cryptolife.net', 'explore.cryptolife.net')
    port = 34821
    message_start = b'\xb8\xfe\xe2\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 33,
        'SCRIPT_ADDR': 20,
        'SECRET_KEY': 161
    }

# no testnet
