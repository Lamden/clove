
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Skeincoin(BitcoinBaseNetwork):
    """
    Class with all the necessary SKC network information based on
    http://www.github.com/skeincoin/skeincoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'skeincoin'
    symbols = ('SKC', )
    seeds = ('seed-a.skeincoin.net', 'seed-b.skeincoin.net', 'seed-c.skeincoin.net', 'seed-d.skeincoin.net',
             'seed-e.skeincoin.net', 'seed-f.skeincoin.net', 'seed-g.skeincoin.net', 'seed-h.skeincoin.net',
             'skein1.ignorelist.com', 'skein2.ignorelist.com', 'skein3.ignorelist.com')
    port = 11230
    message_start = b'\xf7\x26\xa1\xbf'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 12,
        'SECRET_KEY': 226
    }
    source_code_url = 'http://www.github.com/skeincoin/skeincoin/blob/master/src/chainparams.cpp'
