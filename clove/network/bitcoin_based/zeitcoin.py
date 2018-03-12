
from clove.network.bitcoin import Bitcoin


class Zeitcoin(Bitcoin):
    """
    Class with all the necessary ZEIT network information based on
    https://github.com/zeitcoin/zeitcoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'zeitcoin'
    symbols = ('ZEIT', )
    seeds = ('seed.zeit-coin.net', 'zeitseed2.ddns.net', 'seed.aeternity.cc', )
    port = 44845
    message_start = b'\xce\xd5\xdb\xfa'
    base58_prefixes = {
        'PUBKEY_ADDR': 51,
        'SCRIPT_ADDR': 8,
        'SECRET_KEY': 179
    }
