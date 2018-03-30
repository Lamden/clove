
from clove.network.ethereum.base import EthereumBaseNetwork


class SimpleToken(EthereumBaseNetwork):

    name = 'Simple Token'
    symbols = ('ST', )
    token_address = '0x2c4e8f2d746113d0696ce89b35f0d8bf88e0aeca'
