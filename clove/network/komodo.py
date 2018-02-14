from clove.network.bitcoin import Bitcoin


class Komodo(Bitcoin):
    """
    Class with all the necessary KMD network information based on
    https://github.com/jl777/komodo/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'komodo'
    symbols = ('KMD', )
    seeds = (
        'seeds.komodoplatform.com',
        'seeds.komodo.mewhub.com',
    )
    port = 7770
    message_start = b'\xf9\xee\xe4\x8d'
    base58_prefixes = {
        'PUBKEY_ADDR': 60,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 188
    }


class KomodoTestNet(Komodo):
    """
    Class with all the necessary KMD testing network information based on
    https://github.com/jl777/komodo/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-komodo'
    # TODO Gather testing dns seeds
    seeds = ()
    port = 17779
    message_start = b'\x5A\x1F\x7E\x62'
    base58_prefixes = {
        'PUBKEY_ADDR': 0,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }
