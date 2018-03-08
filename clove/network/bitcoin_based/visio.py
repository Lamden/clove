
from clove.network.bitcoin import Bitcoin


class Visio(Bitcoin):
    """
    Class with all the necessary VISIO network information based on
    http://www.github.com/Fladirmacht/visioX/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'visio'
    symbols = ('VISIO', )
    seeds = ('seed.visio.wtf', 'seeda.visio.wtf', 'seedb.visio.wtf',
             'seedc.visio.wtf')
    port = 16778
    message_start = b'\x70\x35\x22\x05'
    base58_prefixes = {
        'PUBKEY_ADDR': 71,
        'SCRIPT_ADDR': 125,
        'SECRET_KEY': 191
    }
