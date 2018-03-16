from clove.network.bitcoin.base import BitcoinBaseNetwork


class Navcoin(BitcoinBaseNetwork):
    """
    Class with all the necessary NAV Coin (NAV) network information based on
    https://github.com/NAVCoin/navcoin-core/blob/master/src/chainparams.cpp
    (date of access: 02/12/2018)
    """
    name = 'navcoin'
    symbols = ('NAV', )
    seeds = ()
    nodes = ('95.183.51.56', '95.183.52.55', '95.183.52.28',
             '95.183.52.29', '95.183.53.184')
    port = 44440
    message_start = b'\x80\x50\x34\x20'
    base58_prefixes = {
        'PUBKEY_ADDR': 53,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 150
    }
    source_code_url = 'https://github.com/NAVCoin/navcoin-core/blob/master/src/chainparams.cpp'
