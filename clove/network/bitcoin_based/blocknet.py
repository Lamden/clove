from clove.network.bitcoin.base import BitcoinBaseNetwork


class Blocknet(BitcoinBaseNetwork):
    """
    Class with all the necessary Blocknet (BLOCK) network information based on
    https://github.com/BlocknetDX/BlockDX/blob/master/src/chainparams.cpp
    (date of access: 02/12/2018)
    """
    name = 'blocknet'
    symbols = ('BLOCK', )
    seeds = ()
    nodes = ('178.62.90.213', '138.197.73.214', '34.235.49.248', )
    port = 41412
    message_start = b'\xa1\xa0\xa2\xa3'
    base58_prefixes = {
        'PUBKEY_ADDR': 26,
        'SCRIPT_ADDR': 28,
        'SECRET_KEY': 154
    }
    source_code_url = 'https://github.com/BlocknetDX/BlockDX/blob/master/src/chainparams.cpp'
