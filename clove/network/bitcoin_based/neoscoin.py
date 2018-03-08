from clove.network.bitcoin import Bitcoin


class Neoscoin(Bitcoin):
    """
    Class with all the necessary Neoscoin (NEOS) network information based on
    https://github.com/neoscoin/neos-core/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'neoscoin'
    symbols = ('NEOS', )
    seeds = ('nodes.neoscoin.com', )
    port = 29320
    message_start = b'\xd3\x1a\x3d\xe4'
    base58_prefixes = {
        'PUBKEY_ADDR': 53,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 177
    }

# no testnet
