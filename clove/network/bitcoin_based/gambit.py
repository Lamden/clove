from clove.network.bitcoin import Bitcoin


class Gambit(Bitcoin):
    """
    Class with all the necessary Gambit (GAM) network information based on
    https://github.com/collincrypto/gambitcrypto/blob/master/src/net.cpp
    (date of access: 02/17/2018)
    """
    name = 'gambit'
    symbols = ('GAM', )
    seeds = ('node1.gambitcrypto.com',
             'node2.gambitcrypto.com', 'node3.gambitcrypto.com')
    port = 47077
    message_start = b'\xf2\xf4\xf6\xf8'
    base58_prefixes = {
        'PUBKEY_ADDR': 38,
        'SCRIPT_ADDR': 97,
        'SECRET_KEY': 166
    }

# no testnet
