from json import JSONDecodeError
from typing import Optional

from bitcoin.core import CTxOut, script
import requests

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
    '''URL for Insight API'''
    ui_url = None
    '''URL for Insight UI'''

    @classmethod
    def get_latest_block(cls) -> Optional[int]:
        '''
        Returns the number of the latest block.

        Returns:
            int, None: number of the latest block or None if API is not working

        Example:
            >>> from clove.network import Bitcoin
            >>> network = Bitcoin()
            >>> network.get_latest_block()
            544989
        '''
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
    def get_transaction(cls, tx_address: str) -> Optional[dict]:
        '''
        Getting transaction details.

        Args:
            tx_address (str): transaction address

        Returns:
            dict, None: dictionary with transaction details or None if transaction doesn't exist

        Example:
            >>> from clove.network import Bitcoin
            >>> network = Bitcoin()
            >>> network.get_transaction('a82213fd237a2b4bf05c805611dc913125aef138bf2874f0668133a4bb5f3b64')
            {'blockhash': '0000000000000000000e2d8d964b4da69f2f30b79aaa58597848719bf0b86a1b',
             'blockheight': 544987,
             'blocktime': 1539068621,
             'confirmations': 3,
             'fees': 0.0011,
             'locktime': 0,
             'size': 192,
             'time': 1539068621,
             'txid': 'a82213fd237a2b4bf05c805611dc913125aef138bf2874f0668133a4bb5f3b64',
             'valueIn': 0.60725408,
             'valueOut': 0.60615408,
             'version': 1,
             'vin': [{'addr': '163o7ig87TnUnp1QF1rBrsjU1uhfEW9nNU',
               'doubleSpentTxID': None,
               'n': 0,
               'scriptSig': {
                'asm': '3045022100ad5db8c05d7f702c8328ae5a817a13dd7f0fda876e3bb3b7729b041bb612275502200af30b833c06c8485ccec95de48c2238a4ffa4e4820dd6466b95dc5d26e883ae[ALL] 03b504de54d5940a81cf5f8c483025c6f39bfc7eed60a022549513fd8d6e41d74f',  # noqa: E50
                'hex': '483045022100ad5db8c05d7f702c8328ae5a817a13dd7f0fda876e3bb3b7729b041bb612275502200af30b833c06c8485ccec95de48c2238a4ffa4e4820dd6466b95dc5d26e883ae012103b504de54d5940a81cf5f8c483025c6f39bfc7eed60a022549513fd8d6e41d74f'},  # noqa: E501
               'sequence': 4294967295,
               'txid': '101cc115cc6882e1fd150c35efd056d18a73c12a3321c406960844561922dfc0',
               'value': 0.60725408,
               'valueSat': 60725408,
               'vout': 0}],
             'vout': [{'n': 0,
               'scriptPubKey': {'addresses': ['13xMGnw7sTTVXT26YpfZQkk2rvuvJFoMvi'],
                'asm': 'OP_DUP OP_HASH160 20680d49e72e1de6af9a0180b3293f2cbd0d0666 OP_EQUALVERIFY OP_CHECKSIG',
                'hex': '76a91420680d49e72e1de6af9a0180b3293f2cbd0d066688ac',
                'type': 'pubkeyhash'},
               'spentHeight': None,
               'spentIndex': None,
               'spentTxId': None,
               'value': '0.60615408'}]}
        '''
        return clove_req_json(f'{cls.api_url}/tx/{tx_address}')

    @classmethod
    def get_utxo(cls, address, amount) -> Optional[list]:
        '''
        Getting list of UTXO objects.

        Args:
            address (str): wallet address to look for UTXO
            amount (float): minimum value that should be satisfied in UTXO objects

        Returns:
            list, None: list of UTXO objects or None it there was not enough UTXO

        Example:
            >>> from clove.network import Litecoin
            >>> network = Litecoin()
            >>> network.get_utxo(address='LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq', amount=0.01)
            [
             Utxo(tx_id='0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec', vout='0', value='0.00976168', tx_script='76a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac', wallet=None, secret=None, refund=False),  # noqa: E501
             Utxo(tx_id='a5c027027c695f403fe570850e35ffd44bb28479ecaaee039372015fe0aae7b2', vout='0', value='0.00097114', tx_script='76a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac', wallet=None, secret=None, refund=False)  # noqa: E501
            ]
        '''
        data = clove_req_json(f'{cls.api_url}/addrs/{address}/utxo')
        if not data:
            logger.debug(f'Cannot find UTXO for address {address} ({cls.symbols[0]})')
            return
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
        '''
        Extracting secret from redeem transaction based on contract address.

        Args:
            contract_address (str): address of the contract atomic swap contract

        Returns:
            str, None: Secret string or None if contract wasn't redeemed yet.

        Example:
            >>> from clove.network import BitcoinTestNet
            >>> network = BitcoinTestNet()
            >>> network.extract_secret_from_redeem_transaction('2N7Gxryn4dD1mdyGM3DMxMAwD7k3RBTJ1gP')
            90f6b9b9a34acb486654b3e9cdc02cce0b8e40a8845924ffda68453ac2477d20
        '''
        contract_transactions = clove_req_json(f'{cls.api_url}/addr/{contract_address}')['transactions']
        if not contract_transactions:
            logger.error(f'Cannot get contract transactions ({cls.symbols[0]})')
            return
        if len(contract_transactions) < 2:
            logger.debug('There is no redeem transaction on this contract yet.')
            return
        redeem_transaction = cls.get_transaction(contract_transactions[0])
        if not redeem_transaction:
            logger.error(f'Cannot get redeem transaction ({cls.symbols[0]})')
            return
        return cls.extract_secret(scriptsig=redeem_transaction['vin'][0]['scriptSig']['hex'])

    @classmethod
    def get_balance(cls, wallet_address: str) -> Optional[float]:
        '''
        Returns wallet balance without unconfirmed transactions.

        Args:
            wallet_address (str): wallet address

        Returns:
            float, None: amount converted from base units or None if something went wrong

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
        '''
        Getting actual fee per kb

        Returns:
            float, None: actual fee per kb or None if eg. API is not responding

        Example:
            >>> from clove.network import BitcoinTestNet
            >>> network = BitcoinTestNet()
            >>> network.get_fee()
            0.00024538
        '''
        try:
            # This endpoint is available from v0.3.1
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
        '''
        Adapter method for returning first vout.

        Args:
            tx_json (dict): dictionary with transaction details

        Returns:
            CTxOut: transaction output
        '''
        cscript = script.CScript.fromhex(tx_json['vout'][0]['scriptPubKey']['hex'])
        nValue = to_base_units(float(tx_json['vout'][0]['value']))
        return CTxOut(nValue, cscript)

    @classmethod
    def publish(cls, raw_transaction: str) -> str:
        '''
        Publish signed transaction via block explorer API.

        Args:
            raw_transaction (str): signed transaction

        Returns:
            str: transaction address if transaction was published

        Raises:
            ValueError: if something went wrong
        '''
        response = requests.post(f'{cls.api_url}/tx/send', data={'rawtx': raw_transaction})
        if response.status_code == 200:
            try:
                return response.json()['txid']
            except (JSONDecodeError, TypeError, KeyError):
                logger.error(f'Unexpected response from API when publishing transaction ({cls.symbols[0]})')
                raise ValueError('Unexpected response format from API. Please try again.')
        if response.status_code == 400:
            logger.debug(f'Error while publishing transaction via API ({cls.symbols[0]}): {response.text}')
            raise ValueError(f'Unexepected error: ({response.text}). Please try again or check your transaction.')
        logger.error(
            f'Unexepected error while publishing transaction via API ({cls.symbols[0]}). '
            'Status code: {response.status.code}'
        )
        raise ValueError('Unexpected response from API. Please try again.')
