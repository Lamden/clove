from clove.network.bitcoin.base import BitcoinBaseNetwork


class SpreadCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary SpreadCoin network information based on
    https://github.com/spreadcoin/spreadcoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'spreadcoin'
    symbols = ('SPR', )
    seeds = ("dnsseed.spreadcoin.net", )
    port = 41678
    message_start = b'\x4f\x3c\x5c\xbb'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 191
    }
    source_code_url = 'https://github.com/spreadcoin/spreadcoin/blob/master/src/net.cpp'
