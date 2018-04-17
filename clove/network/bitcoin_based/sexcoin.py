
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Sexcoin(BitcoinBaseNetwork):
    """
    Class with all the necessary SXC network information based on
    http://www.github.com/sexcoin-project/sexcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'sexcoin'
    symbols = ('SXC', )
    seeds = ('dnsseed.sexcoin.info', 'dnsseed.lavajumper.com', )
    port = 9560
    message_start = b'\xfa\xce\x69\x69'
    base58_prefixes = {
        'PUBKEY_ADDR': 62,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 190
    }
    source_code_url = 'http://www.github.com/sexcoin-project/sexcoin/blob/master/src/chainparams.cpp'


class SexcoinTestNet(Sexcoin):
    """
    Class with all the necessary SXC testing network information based on
    http://www.github.com/sexcoin-project/sexcoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-sexcoin'
    seeds = ('dnsseed.litecoinpool.org', 'testnet-seed.sexcoin.info',
             'testnet-seed.ltc.xurious.com', 'dnsseed.wemine-testnet.com')
    port = 19560
    message_start = b'\xfa\xce\x96\x69'
    base58_prefixes = {
        'PUBKEY_ADDR': 124,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
