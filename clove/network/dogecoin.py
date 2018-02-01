from clove.network.bitcoin import Bitcoin


class Dogecoin(Bitcoin):
    """
    Class with all the necessary DOGE network information based on
    https://github.com/dogecoin/dogecoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'dogecoin'
    symbols = ('DOGE', )
    seeds = (
        'seed.dogecoin.com',
        'seed.multidoge.org',
        'seed2.multidoge.org',
        'seed.doger.dogecoin.com',
    )
    port = 22556


class DogecoinTestNet(Dogecoin):
    """
    Class with all the necessary DOGE testing network information based on
    https://github.com/dogecoin/dogecoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-dogecoin'
    seeds = (
        'testseed.jrn.me.uk',
    )
    port = 44556
