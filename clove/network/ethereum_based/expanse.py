from clove.network.ethereum.base import EthereumBaseNetwork


class Expanse(EthereumBaseNetwork):

    name = 'expanse'
    symbols = ('EXP',)
    web3_provider_address = 'http://gexp.expanse.tech:9656/'
    blockexplorer_tx = 'https://gander.tech/tx/{0}'
    filtering_supported = True

    contract_address = '0x0ff1C3dD4b262a0324910A6E30CaA182204d9163'
