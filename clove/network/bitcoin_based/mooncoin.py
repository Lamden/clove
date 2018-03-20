from clove.network.bitcoin.base import BitcoinBaseNetwork


class Mooncoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Mooncoin (MOON) network information based on
    https://github.com/mooncoincore/wallet/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'mooncoin'
    symbols = ('MOON', )
    seeds = ('node0.bazco.in', 'node1.bazco.in', 'bazco.in')
    port = 44664
    message_start = b'\xf9\xf7\xc0\xe8'
    base58_prefixes = {
        'PUBKEY_ADDR': 3,
        'SCRIPT_ADDR': 22,
        'SECRET_KEY': 131
    }
    source_code_url = 'https://github.com/mooncoincore/wallet/blob/master/src/chainparams.cpp'

# no testnet
