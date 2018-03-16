from clove.network.bitcoin.base import BitcoinBaseNetwork


class Potcoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Potcoin (POT) network information based on
    https://github.com/potcoin/Potcoin/blob/master/src/net.cpp
    (date of access: 02/16/2018)
    """
    name = 'potcoin'
    symbols = ('POT', )
    seeds = ('dnsseedz.potcoin.info', 'dns1.potcoin.info', )
    port = 4200
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 183
    }
