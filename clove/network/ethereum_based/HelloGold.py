
from clove.network.ethereum.base import EthereumBaseNetwork


class HelloGold(EthereumBaseNetwork):

    name = 'HelloGold'
    symbols = ('HGT', )
    token_address = '0xba2184520a1cc49a6159c57e61e1844e085615b6'
