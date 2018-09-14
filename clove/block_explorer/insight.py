from typing import Optional

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class InsightAPI(BaseAPI):
    '''
    Wrapper for block explorers that runs on Insight API engine.
    Docs: https://github.com/satoshilabs/insight-api
    '''

    api_url = None

    @property
    def latest_block(self) -> int:
        return clove_req_json(f'{self.api_url}/api/status')['info']['blocks']

    @classmethod
    def get_transaction(cls, tx_address: str) -> dict:
        return clove_req_json(f'{cls.api_url}/api/tx/{tx_address}')

    @classmethod
    def get_utxo(cls, address, amount):
        data = clove_req_json(f'{cls.api_url}/api/addrs/{address}/utxo')
        unspent = sorted(data, key=lambda k: k['satoshis'], reverse=True)

        utxo = []
        total = 0

        for output in unspent:
            value = from_base_units(output['satoshis'])
            utxo.append(
                Utxo(
                    tx_id=output['txid'],
                    vout=output['vout'],
                    value=value,
                    tx_script=output['scriptPubKey'],
                )
            )
            total += value
            if total > amount:
                return utxo

        logger.debug(f'Cannot find enough UTXO\'s. Found %.8f from %.8f.', total, amount)

    @classmethod
    def extract_secret_from_redeem_transaction(cls, contract_address: str) -> Optional[str]:
        contract_transactions = clove_req_json(f'{cls.api_url}/api/txids/{contract_address}')
        if len(contract_transactions) < 2:
            logger.debug('There is no redeem transaction on this contract yet.')
            return
        redeem_transaction = cls.get_transaction(contract_transactions[1])
        return cls.extract_secret(redeem_transaction['hex'])

    @classmethod
    def get_balance(cls, wallet_address: str) -> float:
        '''
        Returns wallet balance without unconfirmed transactions.

        Args:
            wallet_address (str): wallet address

        Returns:
            float: amount converted from base units

        Example:
            >>> from clove.network import Ravencoin
            >>> r = Ravencoin()
            >>> r.get_balance('RM7w75BcC21LzxRe62jy8JhFYykRedqu8k')
            >>> 18.99
        '''
        wallet_utxo = clove_req_json(f'{cls.api_url}/api/addr/{wallet_address}/balance')
        if not wallet_utxo:
            return 0
        return from_base_units(wallet_utxo)

    @classmethod
    def get_transaction_url(cls, tx_hash: str) -> Optional[str]:
        '''
        Returns URL for a given transaction in block explorer.

        Args:
            tx_hash (str): transaction hash

        Returns:
            str, None: URL for transaction in block explorer or `None` if there is no block explorer

        Example:
            >>> from clove.network import Ravencoin
            >>> r = Ravencoin()
            >>> r.get_transaction_url('8a673e9fcf5ea469e7c4180846834905e8d4c0f16c6e6ab9531efbb9112bc5e1')
            'https://ravencoin.network/tx/8a673e9fcf5ea469e7c4180846834905e8d4c0f16c6e6ab9531efbb9112bc5e1'
        '''
        return f'{cls.api_url}/tx/{tx_hash}'
