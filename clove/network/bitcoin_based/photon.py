
from clove.network.bitcoin import Bitcoin


class Photon(Bitcoin):
    """
    Class with all the necessary PHO network information based on
    http://www.github.com/photonproject/photon/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'photon'
    symbols = ('PHO', )
    seeds = ()
    nodes = ('165.227.200.255', '72.23.74.166', '107.170.219.99', '62.219.234.143', '78.26.209.208',
             '77.121.61.203', '107.170.123.55', '162.243.166.74', '67.205.187.161', '107.170.78.146', '178.62.221.227')
    port = 35556
    message_start = b'\xf9\xbc\xb4\xd2'
    base58_prefixes = {
        'PUBKEY_ADDR': 26,
        'SCRIPT_ADDR': 7,
        'SECRET_KEY': 154
    }


class PhotonTestNet(Photon):
    """
    Class with all the necessary PHO testing network information based on
    http://www.github.com/photonproject/photon/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'test-photon'
    nodes = ()
    seeds = ('photon.info', 'server1.photon.org', 'photon.com', )
    port = 18992
    message_start = b'\x0b\x11\x09\x08'
    base58_prefixes = {
        'PUBKEY_ADDR': 142,
        'SCRIPT_ADDR': 170,
        'SECRET_KEY': 270
    }
