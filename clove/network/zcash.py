from clove.network.bitcoin import Bitcoin


class Zcash(Bitcoin):
    """
    Class with all the necessary ZEC network information based on
    https://github.com/zcash/zcash/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'zcash'
    symbols = ('ZEC', )
    seeds = (
        'dnsseed.z.cash',
        'dnsseed.str4d.xyz',
        'dnsseed.znodes.org',
    )
    port = 18233


class ZcashTestNet(Zcash):
    """
    Class with all the necessary ZEC testing network information based on
    https://github.com/zcash/zcash/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-zcash'
    seeds = (
        'dnsseed.testnet.z.cash',
    )
    port = 18344
