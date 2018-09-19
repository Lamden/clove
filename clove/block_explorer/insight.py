from typing import Optional

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class InsightAPIv4(BaseAPI):
    '''
    Wrapper for block explorers that runs on Insight API engine.
    Docs: https://github.com/bitpay/insight-api/
    '''

    api_url = None
    api_prefix = None

    @classmethod
    def get_latest_block(cls) -> int:
        '''Returns the number of the latest block.'''
        latest_block = clove_req_json(f'{cls.api_url}{cls.api_prefix}/status?q=getInfo')['info']['blocks']
        logger.debug(f'Latest block found: {latest_block}')
        return latest_block

    @classmethod
    def get_latest_block_hash(cls) -> str:
        '''Returns the hash of the latest block.'''
        return clove_req_json(f'{cls.api_url}{cls.api_prefix}/status?q=getLastBlockHash')['lastblockhash']

    @classmethod
    def get_transaction(cls, tx_address: str) -> dict:
        return clove_req_json(f'{cls.api_url}{cls.api_prefix}/tx/{tx_address}')

    @classmethod
    def get_utxo(cls, address, amount):
        data = clove_req_json(f'{cls.api_url}{cls.api_prefix}/addrs/{address}/utxo')
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
        contract_transactions = clove_req_json(f'{cls.api_url}{cls.api_prefix}/txids/{contract_address}')
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
        wallet_utxo = clove_req_json(f'{cls.api_url}{cls.api_prefix}/addr/{wallet_address}/balance')
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

    @classmethod
    def _get_block_hash(cls, block_number: int) -> str:
        '''Getting block hash by its number'''
        block_hash = clove_req_json(f'{cls.api_url}{cls.api_prefix}/block-index/{block_number}')['blockHash']
        logger.debug(f'Found hash for block {block_number}: {block_hash}')
        return block_hash

    @classmethod
    def _get_transactions_from_block(cls, block_number: int):
        '''Getting transactions from block by given block number'''
        block_hash = cls._get_block_hash(block_number)
        transactions_page = clove_req_json(f'{cls.api_url}{cls.api_prefix}/txs/?block={block_hash}')
        transactions = transactions_page['txs']
        logger.debug(f'Found {len(transactions)} in block {block_number}')
        return transactions

    @classmethod
    def _get_transactions(cls):
        '''Getting 10 latest transactions.'''
        from_block = cls.get_latest_block()
        transactions = []
        while len(transactions) < 10:
            block_transactions = cls._get_transactions_from_block(from_block)
            transactions.extend(block_transactions)
            from_block -= 1
            if from_block == 1:
                raise RuntimeError('Not enought number of blocks')
        logger.debug(f'Returning {len(transactions)} transactions')
        return transactions

    @classmethod
    def _callulate_fee(cls):
        '''Calculate fee base on latest transactions'''
        transactions = cls._get_transactions()
        fees = [tx['fees'] for tx in transactions if 'fees' in tx]
        return sum(fees) / len(fees)

    @classmethod
    def get_fee(cls) -> Optional[float]:
        # This endpoint is available from v0.3.1
        fee = clove_req_json(f'{cls.api_url}{cls.api_prefix}/utils/estimatefee?nbBlocks=1')['1']
        logger.debug(f'Incorrect value in estimatedFee: {fee}')
        if fee > 0:
            return fee
        return cls._callulate_fee()
