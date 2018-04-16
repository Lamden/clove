from clove.network.bitcoin.base import BitcoinBaseNetwork


class CreativeCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary CreativeCoin (CREA) network information based on
    https://github.com/creativechain/creativechain-core/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'creativecoin'
    symbols = ('CREA', )
    seeds = ('dnsseed.creativecoin.net', 'creaseed.owldevelopers.site', )
    port = 10946
    message_start = b'\xcc\xcc\xcc\xcc'
    base58_prefixes = {
        'PUBKEY_ADDR': 28,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 176
    }
    source_code_url = 'https://github.com/creativechain/creativechain-core/blob/master/src/chainparams.cpp'


class CreativeCoinTestNet(CreativeCoin):
    """
    Class with all the necessary CreativeCoin (CREA) testing network information based on
    https://github.com/creativechain/creativechain-core/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'test-creativecoin'
    seeds = ('testnet-seed.creativecoin.net', 'tcreaseed.owldevelopers.site', )
    port = 11946
    message_start = b'\xca\xca\xca\xca'
    base58_prefixes = {
        'PUBKEY_ADDR': 87,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
