from clove.network.bitcoin import Bitcoin


class Monacoin(Bitcoin):
    """
    Class with all the necessary MONA network information based on
    https://github.com/monacoinproject/monacoin/blob/master-0.14/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'monacoin'
    symbols = ('MONA', )
    seeds = (
        'dnsseed.monacoin.org',
    )
    port = 9401
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 50,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 176
    }


class MonacoinTestNet(Monacoin):
    """
    Class with all the necessary MONA testing network information based on
    https://github.com/monacoinproject/monacoin/blob/master-0.14/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-monacoin'
    seeds = (
        'testnet-dnsseed.monacoin.org',
    )
    port = 19403
    message_start = b'\xfd\xd2\xc8\xf1'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
