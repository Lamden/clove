from clove.network.base import BaseNetwork


class Zclassic(BaseNetwork):
    """
    Class with all the necessary ZCL network information based on
    https://github.com/z-classic/zclassic/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'zclassic'
    symbols = ('ZCL', )
    seeds = ()
    port = 8033


class TestNetZclassic(Zclassic):
    """
    Class with all the necessary ZCL testing network information based on
    https://github.com/z-classic/zclassic/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-zclassic'
    port = 18233
