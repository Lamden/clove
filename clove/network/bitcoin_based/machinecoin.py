
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Machinecoin(BitcoinBaseNetwork):
    """
    Class with all the necessary MAC network information based on
    http://www.github.com/machinecoin-project/machinecoin-core/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'machinecoin'
    symbols = ('MAC', )
    seeds = ('dnsseed1.machinecoin.org', )
    port = 40333
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 50,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 178
    }
    source_code_url = 'http://www.github.com/machinecoin-project/machinecoin-core/blob/master/src/chainparams.cpp'


class MachinecoinTestNet(Machinecoin):
    """
    Class with all the necessary MAC testing network information based on
    http://www.github.com/machinecoin-project/machinecoin-core/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-machinecoin'
    seeds = ('dnsseed2.machinecoin.org', 'testnetdnsseed1.machinecoin.org',
             'testnetdnsseed2.machinecoin.org')
    port = 50333
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 53,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 178
    }
    testnet = True
