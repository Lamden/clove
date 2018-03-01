from bitcoin.wallet import CBitcoinSecretError

from clove.network.bitcoin import Bitcoin, auto_switch_params


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
    old_secret_key = 178

    @classmethod
    @auto_switch_params()
    def get_wallet(cls, *args, **kwargs):
        try:
            return super().get_wallet(*args, **kwargs)
        except CBitcoinSecretError:
            cls.base58_prefixes['SECRET_KEY'] = cls.old_secret_key
            return super().get_wallet(*args, **kwargs)


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
