from clove.network.bitcoin.base import BitcoinBaseNetwork


class Dopecoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Dopecoin (DOPE) network information based on
    https://github.com/dopecoin-dev/DopeCoinGold/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'dopecoin'
    symbols = ('DOPE', )
    seeds = ('dnsseed.dopecoin.com', )
    port = 40420
    message_start = b'\xdf\x1c\x13\xf8'
    base58_prefixes = {
        'PUBKEY_ADDR': 30,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 158
    }
    source_code_url = 'https://github.com/dopecoin-dev/DopeCoinGold/blob/master/src/chainparams.cpp'

# no testnet
