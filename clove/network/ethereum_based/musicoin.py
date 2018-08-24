from clove.network.ethereum.base import EthereumBaseNetwork


class Musicoin(EthereumBaseNetwork):

    name = 'musicoin'
    symbols = ('MUSIC',)
    web3_provider_address = 'https://mcdnode.trustfarm.io/api'
    blockexplorer_tx = 'https://explorer.musicoin.org/tx/{0}'
    filtering_supported = True

    contract_address = '0x0fa07884343f936AeC6D15229c9481F8100d7c74'
