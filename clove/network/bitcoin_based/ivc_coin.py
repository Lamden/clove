from clove.network.bitcoin.base import BitcoinBaseNetwork


class IVCCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary IVC_Coin network information based on
    https://github.com/invictus2082/invictus/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'ivc_Coin'
    symbols = ('IVC', )
    seeds = ("wallet.cryptolife.net",
             "explore.cryptolife.net",
             "seed1.cryptolife.net",
             "seed2.cryptolife.net")
    port = 41184
    message_start = b'\xde\xca\xa4\xeb'
    base58_prefixes = {
        'PUBKEY_ADDR': 102,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 117
    }
    source_code_url = 'https://github.com/invictus2082/invictus/blob/master/src/chainparams.cpp'

# no testnet
