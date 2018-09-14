import os
from typing import Optional

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class CryptoidAPI(BaseAPI):

    api_url = 'https://chainz.cryptoid.info'

    @classmethod
    def cryptoid_url(cls):
        return f'{cls.api_url}/{cls.symbols[0].lower()}'

    @property
    def latest_block(self) -> int:
        return clove_req_json(f'{self.cryptoid_url()}/api.dws?q=getblockcount')

    @classmethod
    def get_transaction(cls, tx_address: str) -> dict:
        return clove_req_json(f'{cls.cryptoid_url()}/api.dws?q=txinfo&t={tx_address}')

    @classmethod
    def get_utxo(cls, address: str, amount: float):
        api_key = os.environ.get('CRYPTOID_API_KEY')
        if not api_key:
            raise ValueError('API key for cryptoid is required to get UTXOs.')
        data = clove_req_json(f'{cls.cryptoid_url()}/api.dws?q=unspent&key={api_key}&active={address}')
        unspent = data.get('unspent_outputs', [])

        for output in unspent:
            output['value'] = int(output['value'])

        unspent = sorted(unspent, key=lambda k: k['value'], reverse=True)

        utxo = []
        total = 0

        for output in unspent:
            value = from_base_units(output['value'])
            utxo.append(
                Utxo(
                    tx_id=output['tx_hash'],
                    vout=output['tx_ouput_n'],
                    value=value,
                    tx_script=output['script'],
                )
            )
            total += value
            if total > amount:
                return utxo

        logger.debug(f'Cannot find enough UTXO\'s. Found %.8f from %.8f.', total, amount)

    @classmethod
    def extract_secret_from_redeem_transaction(cls, contract_address: str) -> Optional[str]:
        api_key = os.environ.get('CRYPTOID_API_KEY')
        if not api_key:
            raise ValueError('API key for cryptoid is required.')

        data = clove_req_json(f'{cls.cryptoid_url()}/api.dws?q=multiaddr&active={contract_address}&key={api_key}')
        if not data:
            logger.debug('Unexpected response from cryptoid')
            raise ValueError('Unexpected response from cryptoid')

        transactions = data['txs']
        if len(transactions) == 1:
            logger.debug('Contract was not redeemed yet.')
            return

        redeem_tx_hash = transactions[0]['hash']
        logger.warning('Using undocumented endpoint used by chainz.cryptoid.info site.')
        data = clove_req_json(f'{cls.api_url}/explorer/tx.raw.dws?coin={cls.symbols[0].lower()}&id={redeem_tx_hash}')
        if not data:
            logger.debug('Unexpected response from cryptoid')
            raise ValueError('Unexpected response from cryptoid')

        return cls.extract_secret(scriptsig=data['vin'][0]['scriptSig']['hex'])

    @classmethod
    def get_balance(cls, wallet_address: str) -> float:
        api_key = os.environ.get('CRYPTOID_API_KEY')
        if api_key is None:
            raise ValueError('API key for cryptoid is required to get balance.')
        data = clove_req_json(f'{cls.cryptoid_url()}/api.dws?q=getbalance&a={wallet_address}&key={api_key}')
        if data is None:
            logger.debug('Could not get details for address %s in %s network', wallet_address, cls.symbols[0])
            return
        return data

    @classmethod
    def get_transaction_url(cls, tx_hash: str) -> Optional[str]:
        return f'{cls.api_url}/{cls.symbols[0].lower()}/tx.dws?{tx_hash}.htm'
