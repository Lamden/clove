from typing import Optional

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class MonacoinAPI(BaseAPI):

    api_url = 'https://mona.chainseeker.info'

    @property
    def latest_block(self):
        return clove_req_json(f'{self.api_url}/api/v1/status')['blocks']

    @classmethod
    def get_transaction(cls, tx_address: str) -> dict:
        return clove_req_json(f'{cls.api_url}/api/v1/tx/{tx_address}')

    @classmethod
    def get_utxo(cls, address, amount):
        data = clove_req_json(f'{cls.api_url}/api/v1/utxos/{address}')
        unspent = sorted(data, key=lambda k: k['value'], reverse=True)

        utxo = []
        total = 0

        for output in unspent:
            value = from_base_units(output['value'])
            utxo.append(
                Utxo(
                    tx_id=output['txid'],
                    vout=output['vout'],
                    value=value,
                    tx_script=output['scriptPubKey']['hex'],
                )
            )
            total += value
            if total > amount:
                return utxo

        logger.debug(f'Cannot find enough UTXO\'s. Found %.8f from %.8f.', total, amount)

    @classmethod
    def extract_secret_from_redeem_transaction(cls, contract_address: str) -> Optional[str]:
        contract_transactions = clove_req_json(f'{cls.api_url}/api/v1/txids/{contract_address}')
        if len(contract_transactions) < 2:
            logger.debug('There is no redeem transaction on this contract yet.')
            return
        redeem_transaction = cls.get_transaction(contract_transactions[1])
        return cls.extract_secret(redeem_transaction['hex'])

    @classmethod
    def get_balance(cls, wallet_address: str) -> float:
        wallet_utxo = clove_req_json(f'{cls.api_url}/api/v1/utxos/{wallet_address}')
        if not wallet_utxo:
            return 0
        return from_base_units(sum([utxo['value'] for utxo in wallet_utxo]))

    @classmethod
    def get_transaction_url(cls, tx_hash: str) -> Optional[str]:
        return f'{cls.api_url}/tx/{tx_hash}'
