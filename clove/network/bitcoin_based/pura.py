from clove.network.bitcoin.base import BitcoinBaseNetwork


class Pura(BitcoinBaseNetwork):
    """
    Class with all the necessary Pura (PURA) network information based on
    https://github.com/puracore/pura/blob/master/src/chainparamsseeds.h
    (date of access: 02/22/2018)
    """
    name = 'pura'
    symbols = ('PURA', )
    seeds = ()
    nodes = ('45.77.86.242',
             '45.77.69.239',
             '45.32.95.204',
             '45.76.76.71',
             '108.61.216.214',
             '108.61.224.148',
             '45.76.234.219',
             '45.32.195.194',
             '45.76.239.44',
             '45.76.238.77',
             '45.32.227.96',
             '45.63.34.144',
             '104.207.157.63',
             '45.63.36.10',
             '45.63.39.150',
             '45.76.27.81',
             '45.63.71.39',
             '45.76.29.95',
             '45.63.79.204',
             '45.76.31.73',
             '45.76.39.112',
             '45.63.42.37',
             '45.32.236.6',
             '108.61.99.76',
             '108.61.99.36',
             '45.77.68.186',
             '45.32.136.107')
    port = 44444
    message_start = b'\xb8\x97\xc5\x43'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 16,
        'SECRET_KEY': 150
    }
    source_code_url = 'https://github.com/puracore/pura/blob/master/src/chainparamsseeds.h'

# no testnet
