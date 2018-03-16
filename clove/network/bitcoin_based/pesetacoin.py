from clove.network.bitcoin.base import BitcoinBaseNetwork


class Pesetacoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Pesetacoin (PTC) network information based on
    https://github.com/FundacionPesetacoin/Pesetacoin-0.9.1-Oficial/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'pesetacoin'
    symbols = ('PTC', )
    seeds = ('dnsseed.pesetacoin.info', )
    port = 16639
    message_start = b'\xc0\xc0\xc0\xc0'
    base58_prefixes = {
        'PUBKEY_ADDR': 47,
        'SCRIPT_ADDR': 22,
        'SECRET_KEY': 175
    }
    source_code_url = 'https://github.com/FundacionPesetacoin/Pesetacoin-0.9.1-Oficial/blob/master/src/chainparams.cpp'
