
from clove.network.ethereum.base import EthereumBaseNetwork


class Bancor(EthereumBaseNetwork):

    name = 'Bancor'
    symbols = ('BNT', )
    token_address = '0x1f573d6fb3f13d689ff844b4ce37794d79a7ff1c'
