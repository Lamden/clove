from clove.network.bitcoin.base import BitcoinBaseNetwork


class Particl(BitcoinBaseNetwork):
    """
    Class with all the necessary Particl PART network information based on
    https://github.com/particl/particl-core/blob/master/src/chainparams.cpp
    (date of access: 02/12/2018)
    """
    name = 'particl'
    symbols = ('PART', )
    seeds = ('mainnet-seed.particl.io',
             'dnsseed-mainnet.particl.io', 'mainnet.particl.io')
    port = 51738
    message_start = b'\xfb\xf2\xef\xb4'
    base58_prefixes = {
        'PUBKEY_ADDR': 56,
        'SCRIPT_ADDR': 60,
        'SECRET_KEY': 108
    }
    source_code_url = 'https://github.com/particl/particl-core/blob/master/src/chainparams.cpp'


class ParticlTestNet(Particl):
    """
    Class with all the necessary Particl PART testing network information based on
    https://github.com/particl/particl-core/blob/master/src/chainparams.cpp
    (date of access: 02/12/2018)
    """
    name = 'test-particl'
    seeds = ('testnet-seed.particl.io', 'dnsseed-testnet.particl.io', )
    port = 51938
    message_start = b'\x08\x11\x05\x0b'
    base58_prefixes = {
        'PUBKEY_ADDR': 118,
        'SCRIPT_ADDR': 122,
        'SECRET_KEY': 46
    }
    testnet = True
