
from clove.network.bitcoin import Bitcoin


class PIVX(Bitcoin):
    """
    Class with all the necessary PIVX network information based on
    http://www.github.com/PIVX-Project/PIVX/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'pivx'
    symbols = ('PIVX', )
    seeds = ('pivx.seed.fuzzbawls.pw', )
    port = 51472
    message_start = b'\x90\xc4\xfd\xe9'
    base58_prefixes = {
        'PUBKEY_ADDR': 30,
        'SCRIPT_ADDR': 13,
        'SECRET_KEY': 212
    }


class PIVXTestNet(PIVX):
    """
    Class with all the necessary PIVX testing network information based on
    http://www.github.com/PIVX-Project/PIVX/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-pivx'
    seeds = (
        'pivx.seed2.fuzzbawls.pw', 'coin-server.com', 's3v3nh4cks.ddns.net',
        'pivx-testnet.seed.fuzzbawls.pw', 'pivx-testnet.seed2.fuzzbawls.pw', 's3v3nh4cks.ddns.net',
    )
    port = 51474
    message_start = b'\x45\x76\x65\xba'
    base58_prefixes = {
        'PUBKEY_ADDR': 139,
        'SCRIPT_ADDR': 19,
        'SECRET_KEY': 239
    }
