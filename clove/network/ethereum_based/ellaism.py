from clove.network.ethereum.base import EthereumBaseNetwork


class Ellaism(EthereumBaseNetwork):

    name = 'ellaism'
    symbols = ('ELLA',)
    web3_provider_address = 'https://jsonrpc.ellaism.org/'
    blockexplorer_tx = 'https://explorer.ellaism.org/tx/{0}'
    filtering_supported = True

    contract_address = '0x0ff1C3dD4b262a0324910A6E30CaA182204d9163'


class EllaismTestnet(Ellaism):

    name = 'ellaism-testnet'
    testnet = True
    web3_provider_address = 'https://jsonrpc.testnet.ellaism.org/'
    blockexplorer_tx = 'https://explorer.testnet.ellaism.org/tx/{0}'
    filtering_supported = True

    contract_address = '0x520E33ac86ba4C32eF75Ef0AEe0653bB93E249a3'
