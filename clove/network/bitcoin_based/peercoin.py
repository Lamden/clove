from clove.network.bitcoin.base import BitcoinBaseNetwork


class Peercoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Peercoin (PPC) network information based on
    https://github.com/peercoin/peercoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'peercoin'
    symbols = ('PPC', )
    seeds = ('seed.peercoin.net', 'seed.ppcoin.net', )
    port = 9901
    message_start = b'\xe6\xe8\xe9\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 117,
        'SECRET_KEY': 183
    }
    source_code_url = 'https://github.com/peercoin/peercoin/blob/master/src/net.cpp'


class PeercoinTestNet(Peercoin):
    """
    Class with all the necessary Peercoin (PPC) testing network information based on
    https://github.com/peercoin/peercoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'test-peercoin'
    seeds = ('tseed.peercoin.net', )
    port = 9903
    message_start = b'\xcb\xf2\xc0\xef'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
