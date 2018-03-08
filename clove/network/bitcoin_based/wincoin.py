
from clove.network.bitcoin import Bitcoin


class Wincoin(Bitcoin):
    """
    Class with all the necessary WC network information based on
    https://github.com/wincoinofficial/wincoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'wincoin'
    symbols = ('WC', )
    seeds = ()
    nodes = ('47.93.229.223',
             '101.132.41.48',
             '120.77.158.232',
             '47.93.229.223',
             '47.88.170.116',
             '47.88.217.132',
             '47.74.189.163',
             '47.88.169.224',
             '47.88.225.112',
             '47.88.231.237',
             '47.74.179.93',
             '47.74.152.146',
             '52.179.6.159',
             '52.179.102.107'
             )
    port = 11610
    message_start = b'\xf9\xbe\xb4\xd9'
    base58_prefixes = {
        'PUBKEY_ADDR': 73,
        'SCRIPT_ADDR': 83,
        'SECRET_KEY': 201
    }
