import os
from typing import Optional

from bitcoin.core import CTxOut, script

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units, to_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class CryptoidAPI(BaseAPI):

    api_url = 'https://chainz.cryptoid.info'

    @classmethod
    def cryptoid_url(cls):
        return f'{cls.api_url}/{cls.symbols[0].lower()}'

    @classmethod
    def get_latest_block(cls) -> int:
        '''Returns the number of the latest block.'''
        return clove_req_json(f'{cls.cryptoid_url()}/api.dws?q=getblockcount')

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

    @classmethod
    def _get_last_transactions(cls) -> Optional[list]:
        transactions = clove_req_json(f'{cls.cryptoid_url()}/api.dws?q=lasttxs')
        return [tx['hash'] for tx in transactions]

    @classmethod
    def _get_transaction_size(cls, tx_hash: str) -> Optional[int]:
        """WARNING: this method is using undocumented endpoint used by chainz.cryptoid.info site."""
        tx_details = clove_req_json(f'{cls.api_url}/explorer/tx.raw.dws?coin={cls.symbols[0].lower()}&id={tx_hash}')
        return tx_details.get('size')

    @classmethod
    def _get_transaction_fee(cls, tx_hash: str) -> Optional[float]:
        tx_details = clove_req_json(f'{cls.cryptoid_url()}/api.dws?q=txinfo&t={tx_hash}')
        return tx_details.get('fees')

    @classmethod
    def get_fee(cls, tx_limit: int=5) -> Optional[float]:
        """Counting fee based on tx_limit transactions (max 10)"""

        last_transactions = cls._get_last_transactions()

        if not last_transactions:
            return

        last_transactions = last_transactions[:tx_limit]

        fees = []

        for tx_hash in last_transactions:

            tx_size = cls._get_transaction_size(tx_hash)
            if not tx_size:
                continue

            tx_fee = cls._get_transaction_fee(tx_hash)
            if not tx_fee:
                continue

            tx_fee_per_kb = (tx_fee * 1000) / tx_size
            fees.append(tx_fee_per_kb)

        return round(sum(fees) / len(fees), 8) if fees else None

    @classmethod
    def get_first_vout_from_tx_json(cls, tx_json: dict) -> CTxOut:
        incorrect_cscript = script.CScript.fromhex(tx_json['outputs'][0]['script'])
        correct_cscript = script.CScript([script.OP_HASH160, list(incorrect_cscript)[2], script.OP_EQUAL])
        nValue = to_base_units(tx_json['outputs'][0]['amount'])
        return CTxOut(nValue, correct_cscript)
