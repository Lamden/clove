from typing import Optional

from bitcoin.core import CTxOut

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class BlockcypherAPI(BaseAPI):

    api_url = 'https://api.blockcypher.com'

    @classmethod
    def blockcypher_url(cls):
        chain = 'test3' if cls.testnet else 'main'
        return f'{cls.api_url}/v1/{cls.symbols[0].lower()}/{chain}'

    @classmethod
    def get_latest_block(cls) -> int:
        '''Returns the number of the latest block.'''
        return clove_req_json(f'{cls.blockcypher_url()}')['height']

    @classmethod
    def get_transaction(cls, tx_address: str) -> dict:
        return clove_req_json(f'{cls.blockcypher_url()}/txs/{tx_address}?includeHex=true')

    @classmethod
    def get_utxo(cls, address: str, amount: float):
        data = clove_req_json(
            f'{cls.blockcypher_url()}/addrs/{address}'
            '?limit=2000&unspentOnly=true&includeScript=true&confirmations=6'
        )
        unspent = data.get('txrefs', [])

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
                    vout=output['tx_output_n'],
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
        data = clove_req_json(f'{cls.blockcypher_url()}/addrs/{contract_address}/full')
        if not data:
            logger.error('Unexpected response from blockcypher')
            raise ValueError('Unexpected response from blockcypher')

        transactions = data['txs']
        if len(transactions) == 1:
            logger.debug('Contract was not redeemed yet.')
            return

        return cls.extract_secret(scriptsig=transactions[0]['inputs'][0]['script'])

    @classmethod
    def get_balance(cls, wallet_address: str) -> Optional[float]:
        data = clove_req_json(f'{cls.blockcypher_url()}/addrs/{wallet_address}/balance')
        if data is None:
            logger.error('Could not get details for address %s in %s network', wallet_address, cls.symbols[0])
            return
        return from_base_units(data['balance'] or data['unconfirmed_balance'])

    @classmethod
    def get_transaction_url(cls, tx_hash: str) -> Optional[str]:
        if cls.testnet:
            network_name = f'{cls.symbols[0].lower()}-testnet'
        else:
            network_name = cls.symbols[0].lower()
        url = cls.api_url.replace('api.', 'live.')
        return f'{url}/{network_name}/tx/{tx_hash}/'

    @classmethod
    def get_fee(cls) -> Optional[float]:
        '''Returns actual fee per kb.'''
        response = clove_req_json(cls.blockcypher_url())
        fee = response.get('high_fee_per_kb')
        if not fee:
            logger.error('Cannot find the right key (high_fee_per_kb) while getting fee in blockcypher.')
            return
        return from_base_units(fee)

    @classmethod
    def get_first_vout_from_tx_json(cls, tx_json: dict) -> CTxOut:
        tx = cls.deserialize_raw_transaction(tx_json['hex'])
        return tx.vout[0]
