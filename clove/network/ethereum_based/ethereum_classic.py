from clove.network.ethereum.base import EthereumBaseNetwork


class EthereumClassic(EthereumBaseNetwork):

    name = 'ethereum-classic'
    symbols = ('ETC',)
    web3_provider_address = 'https://etc-geth.0xinfra.com/'
    blockexplorer_tx = 'http://gastracker.io/tx/{0}'
    filtering_supported = True

    contract_address = '0x0fF1CEd0d5525a331E562C7c79186045b4D98CFA'
