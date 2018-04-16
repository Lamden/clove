
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Zoin(BitcoinBaseNetwork):
    """
    Class with all the necessary ZOI network information based on
    http://www.github.com/zoinofficial/zoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'zoin'
    symbols = ('ZOI', )
    seeds = ('node11.zoinofficial.com', 'node1.zoinofficial.com',
             'node2.zoinofficial.com', 'node3.zoinofficial.com', 'node4.zoinofficial.com')
    port = 8255
    message_start = b'\xf5\x03\xa9\x51'
    base58_prefixes = {
        'PUBKEY_ADDR': 80,
        'SCRIPT_ADDR': 7,
        'SECRET_KEY': 208
    }
    source_code_url = 'http://www.github.com/zoinofficial/zoin/blob/master/src/chainparams.cpp'


class ZoinTestNet(Zoin):
    """
    Class with all the necessary ZOI testing network information based on
    http://www.github.com/zoinofficial/zoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-zoin'
    seeds = (
        'node5.zoinofficial.com', 'node1.zoinofficial.com', 'node2.zoinofficial.com', 'node3.zoinofficial.com',
        'node4.zoinofficial.com', 'node5.zoinofficial.com', 'node6.zoinofficial.com', 'node7.zoinofficial.com',
        'node8.zoinofficial.com', 'node9.zoinofficial.com', 'node10.zoinofficial.com',
        'seed.tbtc.petertodd.org', 'testnet-seed.bluematt.me', 'testnet-seed.bitcoin.schildbach.de'
    )
    port = 28168
    message_start = b'\xae\x5d\xbf\x09'
    base58_prefixes = {
        'PUBKEY_ADDR': 65,
        'SCRIPT_ADDR': 178,
        'SECRET_KEY': 193
    }
    testnet = True
