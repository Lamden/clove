from clove.network.bitcoin.base import BitcoinBaseNetwork


class Litecoin(BitcoinBaseNetwork):
    """
    Class with all the necessary LTC network information based on
    https://github.com/litecoin-project/litecoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'litecoin'
    symbols = ('LTC', )
    seeds = (
        'seed-a.litecoin.loshan.co.uk',
        # 'dnsseed.thrasher.io', Last check: 2018-02-21
        'dnsseed.litecointools.com',
        'dnsseed.litecoinpool.org',
        'dnsseed.koin-project.com',
    )
    port = 9333
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 48,
        'SCRIPT_ADDR': 50,
        'SECRET_KEY': 176
    }
    source_code_url = 'https://github.com/litecoin-project/litecoin/blob/master/src/chainparams.cpp'


class LitecoinTestNet(Litecoin):
    """
    Class with all the necessary LTC testing network information based on
    https://github.com/litecoin-project/litecoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-litecoin'
    seeds = (
        'testnet-seed.litecointools.com',
        # 'seed-b.litecoin.loshan.co.uk', Last check: 2018-02-21
        # 'dnsseed-testnet.thrasher.io', Last check: 2018-02-21
    )
    port = 19335
    message_start = b'\xfd\xd2\xc8\xf1'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 58,
        'SECRET_KEY': 239
    }
    testnet = True
