
from clove.network.bitcoin.base import BitcoinBaseNetwork


class ZCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary XZC network information based on
    http://www.github.com/zcoinofficial/zcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'zcoin'
    symbols = ('XZC', )
    seeds = ('sf1.zcoin.io', 'sf2.zcoin.io', 'london.zcoin.io',
             'singapore.zcoin.io', 'nyc.zcoin.io')
    port = 8168
    message_start = b'\xe3\xd9\xfe\xf1'
    base58_prefixes = {
        'PUBKEY_ADDR': 82,
        'SCRIPT_ADDR': 7,
        'SECRET_KEY': 210
    }
    source_code_url = 'http://www.github.com/zcoinofficial/zcoin/blob/master/src/chainparams.cpp'


class ZCoinTestNet(ZCoin):
    """
    Class with all the necessary XZC testing network information based on
    http://www.github.com/zcoinofficial/zcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-zcoin'
    seeds = ('beta1.zcoin.io', 'beta2.zcoin.io', 'testnet-seed.bitcoin.jonasschnelli.ch',
             'seed.tbtc.petertodd.org', 'testnet-seed.bluematt.me', 'testnet-seed.bitcoin.schildbach.de')
    port = 18168
    message_start = b'\xcf\xfc\xbe\xea'
    base58_prefixes = {
        'PUBKEY_ADDR': 65,
        'SCRIPT_ADDR': 178,
        'SECRET_KEY': 185
    }
    testnet = True
