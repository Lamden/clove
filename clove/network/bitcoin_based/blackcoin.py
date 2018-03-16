from clove.network.bitcoin.base import BitcoinBaseNetwork


class BlackCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary BlackCoin network information based on
    https://github.com/CoinBlack/blackcoin/blob/master/src/chainparams.cpp
    (date of access: 02/14/2018)
    """
    name = 'BlackCoin'
    symbols = ('BLK', )
    seeds = ("dnsseed.vasin.nl", )
    port = 15714
    message_start = b'\x70\x35\x22\x05'
    base58_prefixes = {
        'PUBKEY_ADDR': 25,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 153
    }
    source_code_url = 'https://github.com/CoinBlack/blackcoin/blob/master/src/chainparams.cpp'

# Has no testnet
