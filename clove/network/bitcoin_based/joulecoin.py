
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Joulecoin(BitcoinBaseNetwork):
    """
    Class with all the necessary XJO network information based on
    http://www.github.com/joulecoin/joulecoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'joulecoin'
    symbols = ('XJO', )
    seeds = ('seed1.jouleco.in', 'seed2.jouleco.in', 'seed3.jouleco.in',
             'seed4.jouleco.in', 'joulecoin1.chickenkiller.com', 'joulecoin2.crabdance.com')
    port = 26789
    message_start = b'\xa5\xc0\x79\x55'
    base58_prefixes = {
        'PUBKEY_ADDR': 43,
        'SCRIPT_ADDR': 11,
        'SECRET_KEY': 143
    }
    source_code_url = 'http://www.github.com/joulecoin/joulecoin/blob/master/src/chainparams.cpp'
