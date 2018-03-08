from clove.network.bitcoin import Bitcoin


class KingNCoin(Bitcoin):
    """
    Class with all the necessary KingN Coin network information based on
    https://github.com/ulandort/kingncoin-source/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'kingncoin'
    symbols = ('KNC', )
    seeds = ("node.walletbuilders.com", )
    port = 18373
    message_start = b'\xfc\x4c\x87\x36'
    base58_prefixes = {
        'PUBKEY_ADDR': 45,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 173
    }


# Has no testnet
