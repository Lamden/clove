
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Viacoin(BitcoinBaseNetwork):
    """
    Class with all the necessary VIA network information based on
    http://www.github.com/viacoin/viacoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'viacoin'
    symbols = ('VIA', )
    seeds = ('seed.viacoin.net', 'viaseeder.barbatos.fr',
             'seed.zzy.su', 'mainnet.viacoin.net')
    port = 5223
    message_start = b'\x0f\x68\xc6\xcb'
    base58_prefixes = {
        'PUBKEY_ADDR': 71,
        'SCRIPT_ADDR': 33,
        'SECRET_KEY': 199
    }
    source_code_url = 'http://www.github.com/viacoin/viacoin/blob/master/src/chainparams.cpp'


class ViacoinTestNet(Viacoin):
    """
    Class with all the necessary VIA testing network information based on
    http://www.github.com/viacoin/viacoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-viacoin'
    seeds = ()
    nodes = ('159.203.109.115', '104.131.34.150', )
    port = 25223
    message_start = b'\xa9\xc5\xef\x92'
    base58_prefixes = {
        'PUBKEY_ADDR': 127,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 255
    }
    testnet = True
