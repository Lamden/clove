from clove.network.bitcoin import Bitcoin


class Litecoin(Bitcoin):
    """
    Class with all the necessary LTC network information based on
    https://github.com/litecoin-project/litecoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'litecoin'
    symbols = ('LTC', )
    seeds = (
        'seed-a.litecoin.loshan.co.uk',
        'dnsseed.thrasher.io',
        'dnsseed.litecointools.com',
        'dnsseed.litecoinpool.org',
        'dnsseed.koin-project.com',
    )
    port = 9333
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 48,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 176
    }


class LitecoinTestNet(Litecoin):
    """
    Class with all the necessary LTC testing network information based on
    https://github.com/litecoin-project/litecoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-litecoin'
    seeds = (
        'testnet-seed.litecointools.com',
        'seed-b.litecoin.loshan.co.uk',
        'dnsseed-testnet.thrasher.io',
    )
    port = 19335
    message_start = b'\xfd\xd2\xc8\xf1'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
