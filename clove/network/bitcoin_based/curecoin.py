from clove.network.bitcoin.base import BitcoinBaseNetwork


class Curecoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Curecoin network information based on
    https://github.com/cygnusxi/curecoinsource/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'curecoin'
    symbols = ('CURE', )
    seeds = ("seed.curecoin.net", "seed2.curecoin.net", )
    port = 9911
    message_start = b'\xe4\xe8\xe9\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 25,
        'SCRIPT_ADDR': 30,
        'SECRET_KEY': 253
    }
    source_code_url = 'https://github.com/cygnusxi/curecoinsource/blob/master/src/net.cpp'


# Has no Testnet
