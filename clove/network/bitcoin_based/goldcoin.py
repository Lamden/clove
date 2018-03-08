from clove.network.bitcoin import Bitcoin


class Goldcoin(Bitcoin):
    """
    Class with all the necessary Goldcoin network information based on
    https://github.com/dmdcoin/diamond/blob/master/src/chainparams.cpp
    (date of access: 02/15/2018)
    """
    name = 'goldcoin'
    symbols = ('GLD', )
    seeds = ("seed.gldcoin.com", "vps.gldcoin.com", )
    port = 8121
    message_start = b'\xe4\xe8\xbd\xfd'
    base58_prefixes = {
        'PUBKEY_ADDR': 90,
        'SCRIPT_ADDR': 8,
        'SECRET_KEY': 218
    }

# no testnet
