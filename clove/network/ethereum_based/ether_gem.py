from clove.network.ethereum.base import EthereumBaseNetwork


class EtherGem(EthereumBaseNetwork):

    name = 'ethergem'
    symbols = ('EGEM',)
    web3_provider_address = 'https://jsonrpc.egem.io/custom'
    blockexplorer_tx = 'https://explorer.egem.io/tx/{0}'
    filtering_supported = True

    contract_address = '0x16F6e3a898dE8d03D9228E0A00e76FeF32868Aa9'
