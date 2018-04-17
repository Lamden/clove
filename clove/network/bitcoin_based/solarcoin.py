
from clove.network.bitcoin.base import BitcoinBaseNetwork


class SolarCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary SLR network information based on
    http://www.github.com/onsightit/solarcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'solarcoin'
    symbols = ('SLR', )
    seeds = (
        'dnsseed.solarcoin.org',
        'download.solarcoin.org',
    )
    port = 18188
    message_start = b'\x04\xf1\x04\xfd'
    base58_prefixes = {
        'PUBKEY_ADDR': 18,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 146
    }
    source_code_url = 'http://www.github.com/onsightit/solarcoin/blob/master/src/chainparams.cpp'


class SolarCoinTestNet(SolarCoin):
    """
    Class with all the necessary SLR testing network information based on
    http://www.github.com/onsightit/solarcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-solarcoin'
    seeds = (
        'testnet-seed.solarcointools.com',
        'seed-b.solarcoin.loshan.co.uk',
        'dnsseed-testnet.thrasher.io',
    )
    port = 19335
    message_start = b'\xfd\xd2\xc8\xf1'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
