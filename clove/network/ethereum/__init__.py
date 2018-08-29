import os

from clove.network.ethereum.base import EthereumBaseNetwork
from clove.network.ethereum_based.kovan_tokens import kovan_tokens
from clove.network.ethereum_based.mainnet_tokens import tokens
from clove.utils.external_source import find_redeem_token_transaction_on_etherscan, find_redeem_transaction_on_etherscan
from clove.utils.logging import logger


class Ethereum(EthereumBaseNetwork):

    name = 'ethereum'
    symbols = ('ETH',)
    infura_network = 'mainnet'
    tokens = tokens
    etherscan_api_subdomain = 'api'
    blockexplorer_tx = 'https://etherscan.io/tx/{0}'

    contract_address = '0x0ff1C3dD4b262a0324910A6E30CaA182204d9163'

    @property
    def web3_provider_address(self) -> str:
        token = os.environ.get('INFURA_TOKEN')
        if not token:
            logger.warning('INFURA_TOKEN environment variable was not set.')
            raise ValueError('INFURA_TOKEN environment variable was not set.')
        return f'https://{self.infura_network}.infura.io/{token}'

    def find_redeem_transaction(self, recipient_address: str, contract_address: str, value: int):
        return find_redeem_transaction_on_etherscan(
            recipient_address=recipient_address,
            contract_address=contract_address,
            value=value,
            subdomain=self.etherscan_api_subdomain,
        )

    def find_redeem_token_transaction(self, recipient_address: str, token_address: str, value: int):
        return find_redeem_token_transaction_on_etherscan(
            recipient_address=recipient_address,
            token_address=token_address,
            value=value,
            subdomain=self.etherscan_api_subdomain,
        )


class EthereumTestnet(Ethereum):

    name = 'test-ethereum'
    infura_network = 'kovan'
    tokens = kovan_tokens
    testnet = True
    etherscan_api_subdomain = 'api-kovan'
    blockexplorer_tx = 'https://kovan.etherscan.io/tx/{0}'

    contract_address = '0xce07aB9477BC20790B88B398A2A9e0F626c7D263'
