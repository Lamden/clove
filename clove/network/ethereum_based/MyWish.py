
from clove.network.ethereum.base import EthereumBaseNetwork


class MyWish(EthereumBaseNetwork):

    name = 'MyWish'
    symbols = ('WISH', )
    token_address = '0x1b22c32cd936cb97c28c5690a0695a82abf688e6'
