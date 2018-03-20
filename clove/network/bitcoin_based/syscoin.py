from clove.network.bitcoin.base import BitcoinBaseNetwork


class Syscoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Syscoin SYS network information based on
    https://github.com/syscoin/syscoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'syscoin'
    symbols = ('SYS', )
    seeds = ('syscoinseed.tk', 'seed.syscoin.tk',
             'seed1.syscoinseed.tk', 'seed2.syscoinseed.tk')
    port = 8369
    message_start = b'\xdc\xec\xec\xdc'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 191
    }
    source_code_url = 'https://github.com/syscoin/syscoin/blob/master/src/net.cpp'
