from typing import Optional

from bitcoin.core import CTxOut

from clove.block_explorer.base import BaseAPI
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class BlockcypherAPI(BaseAPI):
    '''Adapter class for blockcypher.com'''

    api_url = 'https://api.blockcypher.com'
    '''Base url for block explorer API.'''

    @classmethod
    def blockcypher_url(cls) -> str:
        '''
        This method returns a full API url for a given network.

        Returns:
            str: full API url
        '''
        chain = 'test3' if cls.testnet else 'main'
        return f'{cls.api_url}/v1/{cls.symbols[0].lower()}/{chain}'

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
        return clove_req_json(f'{cls.blockcypher_url()}')['height']

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
        return clove_req_json(f'{cls.blockcypher_url()}/txs/{tx_address}?includeHex=true')

    @classmethod
    def get_utxo(cls, address: str, amount: float) -> Optional[list]:
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
        data = clove_req_json(
            f'{cls.blockcypher_url()}/addrs/{address}'
            '?limit=2000&unspentOnly=true&includeScript=true&confirmations=6'
        )
        if not data:
            logger.debug(f'Cannot find UTXO for address {address} ({cls.symbols[0]})')
            return
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
        '''
        Returns wallet balance without unconfirmed transactions.

        Args:
            wallet_address (str): wallet address

        Returns:
            float, None: account balance converted from base units or None if something went wrong

        Example:
            >>> from clove.network import BitcoinTestNet
            >>> network = BitcoinTestNet()
            >>> network.get_balance('msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM')
            4.22188744
        '''
        data = clove_req_json(f'{cls.blockcypher_url()}/addrs/{wallet_address}/balance')
        if data is None:
            logger.error('Could not get details for address %s in %s network', wallet_address, cls.symbols[0])
            return
        return from_base_units(data['balance'] or data['unconfirmed_balance'])

    @classmethod
    def get_transaction_url(cls, tx_hash: str) -> str:
        """
        Returns transaction url for a given transaction hash in block explorer.

        Args:
            tx_hash (str): transaction hash

        Returns:
            str: Url to transaction
        """
        if cls.testnet:
            network_name = f'{cls.symbols[0].lower()}-testnet'
        else:
            network_name = cls.symbols[0].lower()
        url = cls.api_url.replace('api.', 'live.')
        return f'{url}/{network_name}/tx/{tx_hash}/'

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
        response = clove_req_json(cls.blockcypher_url())
        fee = response.get('high_fee_per_kb')
        if not fee:
            logger.error('Cannot find the right key (high_fee_per_kb) while getting fee in blockcypher.')
            return
        return from_base_units(fee)

    @classmethod
    def get_first_vout_from_tx_json(cls, tx_json: dict) -> CTxOut:
        '''
        Adapter method for returning first vout.

        Args:
            tx_json (dict): dictionary with transaction details

        Returns:
            CTxOut: transaction output
        '''
        tx = cls.deserialize_raw_transaction(tx_json['hex'])
        return tx.vout[0]
