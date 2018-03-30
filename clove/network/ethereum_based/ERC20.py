
from clove.network.ethereum.base import EthereumBaseNetwork


class ERC20(EthereumBaseNetwork):

    name = 'ERC20'
    symbols = ('ERC', )
    token_address = '0x26d5bd2dfeda983ecd6c39899e69dae6431dffbb'
