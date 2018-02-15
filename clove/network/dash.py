from clove.network.bitcoin import Bitcoin


class Dash(Bitcoin):
    """
    Class with all the necessary DASH network information based on
    https://github.com/dashpay/dash/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'dash'
    symbols = ('DASH', )
    seeds = (
        'dnsseed.dash.org',
        'dnsseed.dashdot.io',
        'dnsseed.masternode.io',
        'dnsseed.dashpay.io',
    )
    port = 9999
    message_start = b'\xbf\x0c\x6b\xbd'
    base58_prefixes = {
        'PUBKEY_ADDR': 76,
        'SCRIPT_ADDR': 16,
        'SECRET_KEY': 204
    }


class DashTestNet(Dash):
    """
    Class with all the necessary DASH testing network information based on
    https://github.com/dashpay/dash/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-dash'
    seeds = (
        'testnet-seed.dashdot.io',
        'test.dnsseed.masternode.io',
    )
    port = 19999
    message_start = b'\xce\xe2\xca\xff'
    base58_prefixes = {
        'PUBKEY_ADDR': 140,
        'SCRIPT_ADDR': 19,
        'SECRET_KEY': 239
    }
