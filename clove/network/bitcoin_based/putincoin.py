from clove.network.bitcoin import Bitcoin


class PutinCoin(Bitcoin):
    """
    Class with all the necessary PutinCoin network information based on
    https://github.com/putincoinput/putincoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'putincoin'
    symbols = ('PUT', )
    seeds = ()
    nodes = ("45.76.1.121", "45.76.187.49", )
    port = 20095
    message_start = b'\xb7\xf0\xe2\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 20,
        'SECRET_KEY': 183
    }
