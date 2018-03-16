from clove.network.bitcoin.base import BitcoinBaseNetwork


class ToaCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary ToaCoin network information based on
    https://github.com/toacoin/TOA/blob/master/src/net.cpp
    (date of access: 02/15/2018)
    """
    name = 'toacoin'
    symbols = ('TOA', )
    seeds = ()
    nodes = ("212.24.111.232",
             "212.24.111.8",
             "212.24.111.34")
    port = 9642
    message_start = b'\xea\xaf\xe3\xc7'
    base58_prefixes = {
        'PUBKEY_ADDR': 65,
        'SCRIPT_ADDR': 23,
        'SECRET_KEY': 193
    }

# no test net
