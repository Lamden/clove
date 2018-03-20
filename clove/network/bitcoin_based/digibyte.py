from clove.network.bitcoin.base import BitcoinBaseNetwork


class Digibyte(BitcoinBaseNetwork):
    """
    Class with all the necessary DGB network information based on
    https://github.com/digibyte/digibyte/blob/master/src/chainparams.cpp
    (date of access: 02/12/2018)
    """
    name = 'digibyte'
    symbols = ('DGB', )
    seeds = ('seed.digibyte.io', 'digiexplorer.info',
             'digihash.co', 'seed.digibyteprojects.com')
    port = 12024
    message_start = b'\xfa\xc3\xb6\xda'
    base58_prefixes = {
        'PUBKEY_ADDR': 30,
        'SCRIPT_ADDR': 63,
        'SECRET_KEY': 128
    }
    source_code_url = 'https://github.com/digibyte/digibyte/blob/master/src/chainparams.cpp'
