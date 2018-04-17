
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Eternity(BitcoinBaseNetwork):
    """
    Class with all the necessary ENT network information based on
    http://www.github.com/eternity-group/eternity/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'eternity'
    symbols = ('ENT', )
    seeds = ('dnsseed.eternity-group.org', )
    port = 4855
    message_start = b'\x8f\xf7\x4d\x2e'
    base58_prefixes = {
        'PUBKEY_ADDR': 33,
        'SCRIPT_ADDR': 8,
        'SECRET_KEY': 101
    }
    source_code_url = 'http://www.github.com/eternity-group/eternity/blob/master/src/chainparams.cpp'


class EternityTestNet(Eternity):
    """
    Class with all the necessary ENT testing network information based on
    http://www.github.com/eternity-group/eternity/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-eternity'
    seeds = ()
    nodes = ('144.76.33.134', )
    port = 14855
    message_start = b'\xc3\xb3\xea\x5b'
    base58_prefixes = {
        'PUBKEY_ADDR': 93,
        'SCRIPT_ADDR': 10,
        'SECRET_KEY': 239
    }
    testnet = True
