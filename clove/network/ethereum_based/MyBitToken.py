
from clove.network.ethereum.base import EthereumBaseNetwork


class MyBitToken(EthereumBaseNetwork):

    name = 'MyBit Token'
    symbols = ('MyB', )
    token_address = '0x94298f1e0ab2dfad6eeffb1426846a3c29d98090'
