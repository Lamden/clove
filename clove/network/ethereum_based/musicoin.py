from clove.network.ethereum.base import EthereumBaseNetwork


class Musicoin(EthereumBaseNetwork):

    name = 'musicoin'
    symbols = ('MUSIC',)
    web3_provider_address = 'https://mcdnode.trustfarm.io/api'
    blockexplorer_tx = 'https://explorer.musicoin.org/tx/{0}'
    filtering_supported = True

    contract_address = '0x0ff1C3dD4b262a0324910A6E30CaA182204d9163'
