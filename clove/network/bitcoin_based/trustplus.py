from clove.network.bitcoin.base import BitcoinBaseNetwork


class TrustPlus(BitcoinBaseNetwork):
    """
    Class with all the necessary  TrustPlus (TRUST) network information based on
    https://github.com/TrustPlus/TrustPlus/blob/master/src/net.cpp
    (date of access: 02/18/2018)
    """
    name = 'trustplus'
    symbols = ('TRUST', )
    seeds = ()
    nodes = ('104.197.97.72', '23.251.149.70', )
    port = 36999
    message_start = b'\xa1\xa0\xa2\xa3'
    base58_prefixes = {
        'PUBKEY_ADDR': 65,
        'SCRIPT_ADDR': 28,
        'SECRET_KEY': 193
    }
    source_code_url = 'https://github.com/TrustPlus/TrustPlus/blob/master/src/net.cpp'
