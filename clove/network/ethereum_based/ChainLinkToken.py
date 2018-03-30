
from clove.network.ethereum.base import EthereumBaseNetwork


class ChainLinkToken(EthereumBaseNetwork):

    name = 'ChainLink Token'
    symbols = ('LINK', )
    token_address = '0x514910771af9ca656af840dff83e8264ecf986ca'
