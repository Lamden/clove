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
    message_start = b'\xc0\xc0\xc0\xc0'
    base58_prefixes = {
        'PUBKEY_ADDR': 30,
        'SCRIPT_ADDR': 22,
        'SECRET_KEY': 158
    }


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
    message_start = b'\xfc\xc1\xb7\xdc'
    base58_prefixes = {
        'PUBKEY_ADDR': 113,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 241
    }
