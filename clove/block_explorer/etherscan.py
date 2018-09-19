import os
from typing import Optional

from clove.block_explorer.base import BaseAPI
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class EtherscanAPI(BaseAPI):

    def find_redeem_transaction(self, recipient_address: str, contract_address: str, value: int) -> Optional[str]:
        recipient_address = recipient_address.lower()
        contract_address = contract_address.lower()
        value = str(value)

        etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')
        if not etherscan_api_key:
            raise ValueError('API key for etherscan is required.')

        data = clove_req_json(
            f'http://{self.etherscan_api_subdomain}.etherscan.io/api?module=account&action=txlistinternal'
            f'&address={recipient_address}&apikey={etherscan_api_key}'
        )

        for result in reversed(data['result']):
            if result['to'] == recipient_address and result['from'] == contract_address and result['value'] == value:
                return result['hash']

        logger.debug('Redeem transaction not found.')

    def find_redeem_token_transaction(self, recipient_address: str, token_address: str, value: int) -> Optional[str]:
        recipient_address = recipient_address.lower()
        token_address = token_address.lower()
        value = str(value)

        etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')
        if not etherscan_api_key:
            raise ValueError('API key for etherscan is required.')

        data = clove_req_json(
            f'http://{self.etherscan_api_subdomain}.etherscan.io/api?module=account&action=tokentx'
            f'&contractaddress={token_address}&address={recipient_address}'
            f'&apikey={etherscan_api_key}'
        )

        for result in reversed(data['result']):
            if result['to'] == recipient_address \
                    and result['contractAddress'] == token_address \
                    and result['value'] == value:
                return result['hash']

        logger.debug('Redeem token transaction not found.')
