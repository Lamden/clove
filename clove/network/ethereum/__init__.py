from clove.network.ethereum.base import EthereumBaseNetwork


class Ethereum(EthereumBaseNetwork):

    name = 'ethereum'
    symbols = ('ETH',)
    infura_network = 'mainnet'


class EthereumTestnet(Ethereum):

    name = 'testnet-ethereum'
    infura_network = 'kovan'

    eth_swap_contract_address = '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8'
    token_swap_contract_address = '0x7657Ca877Fac31D20528B473162E39B6E152fd2e'
