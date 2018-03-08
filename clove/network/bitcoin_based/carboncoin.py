
from clove.network.bitcoin import Bitcoin


class Carboncoin(Bitcoin):
    """
    Class with all the necessary CARBON network information based on
    http://www.github.com/carboncointrust/CarboncoinCore/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'carboncoin'
    symbols = ('CARBON', )
    seeds = ('dnsseed.sequestrationcoin.com', 'dnsmain.sequestrationcoin.com', )
    port = 9350
    message_start = b'\xab\xcc\xbb\xdf'
    base58_prefixes = {
        'PUBKEY_ADDR': 47,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 175
    }


class CarboncoinTestNet(Carboncoin):
    """
    Class with all the necessary CARBON testing network information based on
    http://www.github.com/carboncointrust/CarboncoinCore/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-carboncoin'
    seeds = ('dnsseed.sequestrationcoin.com', 'dnstest.sequestrationcoin.com', )
    port = 19350
    message_start = b'\xfc\xc1\xb7\xdc'
    base58_prefixes = {
        'PUBKEY_ADDR': 113,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 241
    }
