
from clove.network.bitcoin import Bitcoin


class BitTokens(Bitcoin):
    """
    Class with all the necessary BXT network information based on
    http://www.github.com/BitTokens/BitToken/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'bittokens'
    symbols = ('BXT', )
    seeds = ('node.walletbuilders.com', )
    port = 8223
    message_start = b'\x57\xab\xdb\x52'
    base58_prefixes = {
        'PUBKEY_ADDR': 25,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 153
    }
