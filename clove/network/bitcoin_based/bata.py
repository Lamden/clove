
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Bata(BitcoinBaseNetwork):
    """
    Class with all the necessary BTA network information based on
    http://www.github.com/BTA-BATA/BATA-SOURCE/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'bata'
    symbols = ('BTA', )
    seeds = ('list.batadnsseed.bata.io', 'batadnsseed.midnightminer.net', )
    port = 5784
    message_start = b'\x34\xc3\xaf\xeb'
    base58_prefixes = {
        'PUBKEY_ADDR': 25,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 188
    }
    source_code_url = 'http://www.github.com/BTA-BATA/BATA-SOURCE/blob/master/src/chainparams.cpp'


class BataTestNet(Bata):
    """
    Class with all the necessary BTA testing network information based on
    http://www.github.com/BTA-BATA/BATA-SOURCE/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-bata'
    seeds = ('testnet-seed.bata.io', 'testnet-bata.midnightminer.net',
             'dnsseed.wemine-testnet.com')
    port = 33813
    message_start = b'\xba\xad\xaf\xc5'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
