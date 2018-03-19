
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Unobtanium(BitcoinBaseNetwork):
    """
    Class with all the necessary UNO network information based on
    http://www.github.com/unobtanium-official/Unobtanium/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'unobtanium'
    symbols = ('UNO', )
    seeds = ('node1.unobtanium.uno', 'node2.unobtanium.uno',
             'unobtanium.cryptap.us')
    port = 65534
    message_start = b'\x03\xd5\xb5\x03'
    base58_prefixes = {
        'PUBKEY_ADDR': 130,
        'SCRIPT_ADDR': 30,
        'SECRET_KEY': 224
    }


class UnobtaniumTestNet(Unobtanium):
    """
    Class with all the necessary UNO testing network information based on
    http://www.github.com/unobtanium-official/Unobtanium/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-unobtanium'
    seeds = ('23skidoo.info', 'testnet.unobtanium.info', )
    port = 65525
    message_start = b'\x01\x02\x03\x04'
    base58_prefixes = {
        'PUBKEY_ADDR': 68,
        'SCRIPT_ADDR': 30,
        'SECRET_KEY': 239
    }
