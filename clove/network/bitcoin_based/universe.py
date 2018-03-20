from clove.network.bitcoin.base import BitcoinBaseNetwork


class Universe(BitcoinBaseNetwork):
    """
    Class with all the necessary Universe (UNI) network information based on
    https://github.com/UniverseUNI/Universe-UNI/blob/master/src/net.cpp
    (date of access: 02/17/2018)
    """
    name = 'universe'
    symbols = ('UNI', )
    seeds = ('seed.unicoin.pw', 'seed2.unicoin.pw', )
    port = 11029
    message_start = b'\x57\x46\xf2\x84'
    base58_prefixes = {
        'PUBKEY_ADDR': 68,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 196
    }
    source_code_url = 'https://github.com/UniverseUNI/Universe-UNI/blob/master/src/net.cpp'

# no testnet
