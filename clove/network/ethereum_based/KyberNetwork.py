
from clove.network.ethereum.base import EthereumBaseNetwork


class KyberNetwork(EthereumBaseNetwork):

    name = 'KyberNetwork'
    symbols = ('KNC', )
    token_address = '0xdd974d5c2e2928dea5f71b9825b8b646686bd200'
