from clove.network.bitcoin import Bitcoin


class Prototanium(Bitcoin):
    """
    Class with all the necessary Prototanium network information based on
    https://github.com/Prototanium/Pr/blob/master/src/chainparams.cpp
    (date of access: 02/19/2018)
    """
    name = 'prototanium'
    symbols = ('PR', )
    seeds = ("proto.uno",
             "23skidoo.info")
    port = 65525
    message_start = b'\x01\x02\x03\x04'
    base58_prefixes = {
        'PUBKEY_ADDR': 68,
        'SCRIPT_ADDR': 30,
        'SECRET_KEY': 239
    }


class PrototaniumTestNet(Prototanium):
    """
    Class with all the necessary Prototanium testing network information based on
    https://github.com/Prototanium/Pr/blob/master/src/chainparams.cpp
    (date of access: 02/19/2018)
    """
    name = 'test-prototanium'
    seeds = ("23skidoo.info",
             "testnet.prototanium.info")
    port = 65525
    message_start = b'\x01\x02\x03\x04'
    base58_prefixes = {
        'PUBKEY_ADDR': 68,
        'SCRIPT_ADDR': 30,
        'SECRET_KEY': 239
    }
