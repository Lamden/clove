from clove.network.bitcoin.base import BitcoinBaseNetwork


class Goldcoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Goldcoin network information based on
    https://github.com/goldcoin/goldcoin/blob/master/src/net.cpp
    (date of access: 02/15/2018)
    """
    name = 'goldcoin'
    symbols = ('GLD', )
    seeds = ("seed.gldcoin.com", "vps.gldcoin.com", )
    port = 8121
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 32,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 160
    }
    source_code_url = 'https://github.com/goldcoin/goldcoin/blob/master/src/net.cpp'

# no testnet
