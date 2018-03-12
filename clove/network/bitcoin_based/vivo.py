
from clove.network.bitcoin import Bitcoin


class Vivo(Bitcoin):
    """
    Class with all the necessary VIVO network information based on
    http://www.github.com/vivocoin/vivo/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'vivo'
    symbols = ('VIVO', )
    seeds = ('vivoseed1.vivoseeds.win', )
    port = 12845
    message_start = b'\x1d\x42\x5b\xa7'
    base58_prefixes = {
        'PUBKEY_ADDR': 70,
        'SCRIPT_ADDR': 10,
        'SECRET_KEY': 198
    }
