
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Myriad(BitcoinBaseNetwork):
    """
    Class with all the necessary XMY network information based on
    http://www.github.com/myriadteam/myriadcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'myriad'
    symbols = ('XMY', )
    seeds = ('seed1.myriadcoin.org', 'seed2.myriadcoin.org', 'seed3.myriadcoin.org', 'seed4.myriadcoin.org',
             'seed5.myriadcoin.org', 'seed6.myriadcoin.org', 'seed7.myriadcoin.org', 'seed8.myriadcoin.org',
             'myriadseed1.cryptap.us')
    port = 10888
    message_start = b'\xaf\x45\x76\xee'
    base58_prefixes = {
        'PUBKEY_ADDR': 50,
        'SCRIPT_ADDR': 9,
        'SECRET_KEY': 178
    }
    source_code_url = 'http://www.github.com/myriadteam/myriadcoin/blob/master/src/chainparams.cpp'


class MyriadTestNet(Myriad):
    """
    Class with all the necessary XMY testing network information based on
    http://www.github.com/myriadteam/myriadcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-myriad'
    seeds = ('testseed1.myriadcoin.org', 'myriadtestseed1.cryptap.us', )
    port = 20888
    message_start = b'\x01\xf5\x55\xa4'
    base58_prefixes = {
        'PUBKEY_ADDR': 88,
        'SCRIPT_ADDR': 188,
        'SECRET_KEY': 239
    }
    testnet = True
