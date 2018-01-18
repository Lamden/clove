from clove.network.base import BaseNetwork


class Dash(BaseNetwork):
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


class TestNetDash(Dash):
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
