from clove.network.bitcoin.base import BitcoinBaseNetwork


class Kittehcoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Kittehcoin network information based on
    https://github.com/kittehcoin/kittehcoin/blob/master/src/net.cpp
    (date of access: 02/16/2018)
    """
    name = 'kittehcoin'
    symbols = ('MEOW', )
    seeds = ("dnsseed.kittehcoin.info",
             "dnsseed.kittehcoinwallet.com",
             "dnsseed.kittehcoinblockexplorer.com",
             "dnsseed.kittehcoinpool.com")
    port = 22566
    message_start = b'\xc0\xc0\xc0\xc0'
    base58_prefixes = {
        'PUBKEY_ADDR': 45,
        'SCRIPT_ADDR': 22,
        'SECRET_KEY': 173
    }
    source_code_url = 'https://github.com/kittehcoin/kittehcoin/blob/master/src/net.cpp'
