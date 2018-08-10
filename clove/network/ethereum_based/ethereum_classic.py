from clove.network.ethereum.base import EthereumBaseNetwork
from clove.network.ethereum.token import TokenMixin


class EthereumClassicToken(TokenMixin):

    pass


class EthereumClassic(EthereumBaseNetwork):

    name = 'ethereum-classic'
    symbols = ('ETC',)
    web3_provider_address = 'https://etc-geth.0xinfra.com/'
    blockexplorer_tx = 'http://gastracker.io/tx/{0}'
    token_class = EthereumClassicToken

    contract_address = '0x0fF1CEd0d5525a331E562C7c79186045b4D98CFA'
