from clove.network.bitcoin import Bitcoin


class RSGPcoin(Bitcoin):
    """
    Class with all the necessary RSGPcoin network information based on
    https://github.com/ulandort/rsgprepo/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'rsgpcoin'
    symbols = ('RSGP', )
    seeds = ("node.walletbuilders.com", )
    port = 19529
    message_start = b'\x7c\x55\x0b\x18'
    base58_prefixes = {
        'PUBKEY_ADDR': 60,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 188
    }


# Has no testnet
