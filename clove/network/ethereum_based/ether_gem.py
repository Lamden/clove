from clove.network.ethereum.base import EthereumBaseNetwork


class EtherGem(EthereumBaseNetwork):

    name = 'ethergem'
    symbols = ('EGEM',)
    web3_provider_address = 'https://jsonrpc.egem.io/custom'
    blockexplorer_tx = 'https://explorer.egem.io/tx/{0}'
    filtering_supported = True

    contract_address = '0x0ff1C3dD4b262a0324910A6E30CaA182204d9163'
