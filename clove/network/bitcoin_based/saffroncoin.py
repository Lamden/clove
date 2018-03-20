from clove.network.bitcoin.base import BitcoinBaseNetwork


class Saffroncoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Saffroncoin network information based on
    https://github.com/saffroncoin/saffroncoin/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'saffroncoin'
    symbols = ('SFR', )
    seeds = ("saffroncoin.com", )
    port = 19717
    message_start = b'\xcf\x05\x67\xea'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 177
    }
    source_code_url = 'https://github.com/saffroncoin/saffroncoin/blob/master/src/chainparams.cpp'
