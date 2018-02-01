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
