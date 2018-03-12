
from clove.network.bitcoin import Bitcoin


class Solaris(Bitcoin):
    """
    Class with all the necessary XLR network information based on
    http://www.github.com/Solaris-Project/Solaris/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'solaris'
    symbols = ('XLR', )
    seeds = (
        'solarisnode.dyndns.org', 'solarisnode1.dyndns.org', 'solarisnode2.dyndns.org',
        'solarisnode3.dyndns.org', 'solarisnode4.dyndns.org', 'solarisnode5.dyndns.org',
        'solarisnode6.dyndns.org', 'node1.solariscoin.com', 'node2.solariscoin.com', 'node3.solariscoin.com',
        'node4.solariscoin.com', 'node5.solariscoin.com', 'node6.solariscoin.com'
    )
    port = 60020
    message_start = b'\x02\x21\x01\xa1'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 13,
        'SECRET_KEY': 212
    }


class SolarisTestNet(Solaris):
    """
    Class with all the necessary XLR testing network information based on
    http://www.github.com/Solaris-Project/Solaris/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-solaris'
    seeds = ('solaris-testnet.seed.fuzzbawls.pw',
             'solaris-testnet.seed2.fuzzbawls.pw', 's3v3nh4cks.ddns.net')
    port = 51474
    message_start = b'\x45\x76\x65\xba'
    base58_prefixes = {
        'PUBKEY_ADDR': 139,
        'SCRIPT_ADDR': 19,
        'SECRET_KEY': 239
    }
