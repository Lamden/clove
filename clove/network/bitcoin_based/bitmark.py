from clove.network.bitcoin.base import BitcoinBaseNetwork


class Bitmark(BitcoinBaseNetwork):
    """
    Class with all the necessary Bitmark network information based on
    https://github.com/project-bitmark/bitmark/blob/master/src/chainparams.cpp
    (date of access: 02/14/2018)
    """
    name = 'bitmark'
    symbols = ('BTM', )
    seeds = ("biji.bitmark.one",
             "shido.bitmark.one",
             "ra.zmark.org",
             "shiba.zmark.org",
             "btmk.zmark.org",
             "btmk.bitmark.guru",
             "da.bitmark.guru",
             "da.bitmark.mx",
             "btm.zmark.org")
    port = 9265
    message_start = b'\xf9\xbe\xb4\xd9'
    base58_prefixes = {
        'PUBKEY_ADDR': 85,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 213
    }
    source_code_url = 'https://github.com/project-bitmark/bitmark/blob/master/src/chainparams.cpp'
