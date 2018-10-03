from typing import Optional

from bitcoin.core import CTxOut, script

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units, to_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class InsightAPIv4(BaseAPI):
    '''
    Wrapper for block explorers that runs on Insight API engine.
    Docs: https://github.com/bitpay/insight-api/
    '''

    api_url = None
    ui_url = None

    @classmethod
    def get_latest_block(cls) -> Optional[int]:
        '''Returns the number of the latest block.'''
        try:
            latest_block = clove_req_json(f'{cls.api_url}/status?q=getInfo')['info']['blocks']
        except (TypeError, KeyError):
            logger.error(f'Cannot get latest block, bad response ({cls.symbols[0]})')
            return
        if not latest_block:
            logger.debug(f'Latest block not found ({cls.symbols[0]})')
            return
        logger.debug(f'Latest block found: {latest_block}')
        return latest_block

    @classmethod
    def get_transaction(cls, tx_address: str) -> dict:
        return clove_req_json(f'{cls.api_url}/tx/{tx_address}')

    @classmethod
    def get_utxo(cls, address, amount):
        data = clove_req_json(f'{cls.api_url}/addrs/{address}/utxo')
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
        contract_transactions = clove_req_json(f'{cls.api_url}/txids/{contract_address}')
        if not contract_transactions:
            logger.error(f'Cannot get contract transactions ({cls.symbols[0]})')
            return
        if len(contract_transactions) < 2:
            logger.debug('There is no redeem transaction on this contract yet.')
            return
        redeem_transaction = cls.get_transaction(contract_transactions[1])
        if not redeem_transaction:
            logger.error(f'Cannot get redeem transaction ({cls.symbols[0]})')
            return
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
        wallet_utxo = clove_req_json(f'{cls.api_url}/addr/{wallet_address}/balance')
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
        return f'{cls.ui_url}/tx/{tx_hash}'

    @classmethod
    def _get_block_hash(cls, block_number: int) -> str:
        '''Getting block hash by its number'''
        try:
            block_hash = clove_req_json(f'{cls.api_url}/block-index/{block_number}')['blockHash']
        except (TypeError, KeyError):
            logger.error(f'Cannot get block hash for block {block_number} ({cls.symbols[0]})')
            return
        logger.debug(f'Found hash for block {block_number}: {block_hash}')
        return block_hash

    @classmethod
    def _get_transactions_from_block(cls, block_number: int):
        '''Getting transactions from block by given block number'''
        block_hash = cls._get_block_hash(block_number)
        if not block_hash:
            return
        transactions_page = clove_req_json(f'{cls.api_url}/txs/?block={block_hash}')
        if not transactions_page:
            return
        transactions = transactions_page['txs']
        logger.debug(f'Found {len(transactions)} in block {block_number}')
        return transactions

    @classmethod
    def _get_transactions(cls):
        '''Getting 10 latest transactions.'''
        from_block = cls.get_latest_block()
        if not from_block:
            return
        transactions = []
        errors_counter = 0
        while len(transactions) < 10:
            if errors_counter > 10:
                raise RuntimeError(f'Cannot get transactions from block ({cls.symbols[0]})')
            block_transactions = cls._get_transactions_from_block(from_block)
            if not block_transactions:
                errors_counter += 1
                from_block -= 1
                continue
            transactions.extend(block_transactions)
            from_block -= 1
            if from_block == 1:
                raise RuntimeError(f'Not enought number of blocks ({cls.symbols[0]})')
        logger.debug(f'Returning {len(transactions)} transactions')
        return transactions

    @classmethod
    def _calculate_fee(cls):
        '''Calculate fee base on latest transactions'''
        try:
            transactions = cls._get_transactions()
        except RuntimeError:
            return
        if not transactions:
            return
        fees = [tx['fees'] for tx in transactions if 'fees' in tx]
        return sum(fees) / len(fees)

    @classmethod
    def get_fee(cls) -> Optional[float]:
        # This endpoint is available from v0.3.1
        try:
            fee = clove_req_json(f'{cls.api_url}/utils/estimatefee?nbBlocks=1')['1']
        except (TypeError, KeyError):
            logger.error(
                f'Incorrect response from API when getting fee from {cls.api_url}/utils/estimatefee?nbBlocks=1'
            )
            return cls._calculate_fee()

        if fee == -1:
            logger.debug(f'Incorrect value in estimatedFee: {fee}')
            return cls._calculate_fee()
        fee = float(fee)
        if fee > 0:
            logger.warning(f'Got fee = 0 for ({cls.symbols[0]}), calculating manually')
            return fee
        return cls._calculate_fee()

    @classmethod
    def get_first_vout_from_tx_json(cls, tx_json: dict) -> CTxOut:
        cscript = script.CScript.fromhex(tx_json['vout'][0]['scriptPubKey']['hex'])
        nValue = to_base_units(float(tx_json['vout'][0]['value']))
        return CTxOut(nValue, cscript)
