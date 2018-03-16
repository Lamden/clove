
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Renos(BitcoinBaseNetwork):
    """
    Class with all the necessary RNS network information based on
    http://www.github.com/RenosCoin/RenosCoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'renos'
    symbols = ('RNS', )
    seeds = ('seed.renoscoin.com', 'seed.renos.network', )
    port = 57155
    message_start = b'\xaa\xa3\xb2\xc4'
    base58_prefixes = {
        'PUBKEY_ADDR': 60,
        'SCRIPT_ADDR': 28,
        'SECRET_KEY': 150
    }
    source_code_url = 'http://www.github.com/RenosCoin/RenosCoin/blob/master/src/chainparams.cpp'
