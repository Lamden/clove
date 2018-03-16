from clove.network.bitcoin.base import BitcoinBaseNetwork


class Guncoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Guncoin network information based on
    https://github.com/guncoin/guncoin/blob/master-1.4/src/chainparams.cpp
    (date of access: 02/15/2018)
    """
    name = 'guncoin'
    symbols = ('GUN', )
    seeds = ("seed.guncoin.info", "seed2.guncoin.info", )
    port = 42954
    message_start = b'\xaa\xc3\xc6\xab'
    base58_prefixes = {
        'PUBKEY_ADDR': 39,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 167
    }
    source_code_url = 'https://github.com/guncoin/guncoin/blob/master-1.4/src/chainparams.cpp'
