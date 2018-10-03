from datetime import datetime

from eth_abi import decode_abi
from ethereum.transactions import Transaction
from web3 import Web3
from web3.utils.abi import get_abi_input_names, get_abi_input_types
from web3.utils.contracts import find_matching_fn_abi

from clove.constants import ETH_REDEEM_GAS_LIMIT, ETH_REFUND_GAS_LIMIT
from clove.network.ethereum.transaction import EthereumTokenTransaction
from clove.utils.logging import logger


class EthereumContract(object):

    def __init__(self, network, tx_dict):

        self.network = network
        self.tx_dict = tx_dict
        self.abi = self.network.abi
        self.method_id = self.network.extract_method_id(tx_dict['input'])
        self.type = self.network.get_method_name(self.method_id)
        self.token = None

        if self.method_id != self.network.initiate:
            logger.warning('Not a contract transaction.')
            raise ValueError('Not a contract transaction.')

        input_types = get_abi_input_types(find_matching_fn_abi(self.abi, fn_identifier=self.type))
        input_names = get_abi_input_names(find_matching_fn_abi(self.abi, fn_identifier=self.type))
        input_values = decode_abi(input_types, Web3.toBytes(hexstr=self.tx_dict['input'][10:]))
        self.inputs = dict(zip(input_names, input_values))

        self.locktime = datetime.utcfromtimestamp(self.inputs['_expiration'])
        self.recipient_address = Web3.toChecksumAddress(self.inputs['_participant'])
        self.refund_address = self.tx_dict['from']
        self.secret_hash = self.inputs['_hash'].hex()
        self.contract_address = Web3.toChecksumAddress(self.tx_dict['to'])
        self.block_number = self.tx_dict['blockNumber']
        self.confirmations = self.network.get_latest_block - self.block_number
        self.balance = self.get_balance()

        if self.is_token_contract:
            self.value_base_units = self.inputs['_value']
            self.token_address = Web3.toChecksumAddress(self.inputs['_token'])
            self.token = self.network.get_token_by_address(self.token_address)
            self.value = self.token.value_from_base_units(self.value_base_units)
            self.symbol = self.token.symbol
        else:
            self.value_base_units = self.tx_dict['value']
            self.value = self.network.value_from_base_units(self.value_base_units)
            self.symbol = self.network.default_symbol

    @property
    def is_token_contract(self):
        return self.inputs['_isToken']

    @property
    def contract(self):
        return self.network.web3.eth.contract(
            address=self.contract_address, abi=self.network.abi
        )

    def get_balance(self) -> float:
        contract = self.contract
        contract_swap = contract.functions.swaps(self.recipient_address, self.secret_hash).call()
        contract_exists = contract_swap[-1]
        contract_balance = contract_swap[3]

        if contract_exists:
            return contract_balance
        return 0

    def participate(
        self,
        symbol: str,
        sender_address: str,
        recipient_address: str,
        value: float,
        utxo: list=None,
        token_address: str=None,
    ):
        network = self.network.get_network_by_symbol(symbol)
        if network.ethereum_based:
            return network.atomic_swap(
                sender_address,
                recipient_address,
                str(value),
                self.secret_hash,
                token_address,
            )
        return network.atomic_swap(
            sender_address,
            recipient_address,
            value,
            utxo,
            self.secret_hash,
        )

    def redeem(self, secret: str) -> EthereumTokenTransaction:
        if self.balance == 0:
            raise ValueError("Balance of this contract is 0.")
        contract = self.contract
        redeem_func = contract.functions.redeem(secret)
        tx_dict = {
            'nonce': self.network.web3.eth.getTransactionCount(self.recipient_address),
            'value': 0,
            'gas': ETH_REDEEM_GAS_LIMIT,
        }

        tx_dict = redeem_func.buildTransaction(tx_dict)

        transaction = EthereumTokenTransaction(network=self.network)
        transaction.tx = Transaction(
            nonce=tx_dict['nonce'],
            gasprice=tx_dict['gasPrice'],
            startgas=tx_dict['gas'],
            to=tx_dict['to'],
            value=tx_dict['value'],
            data=Web3.toBytes(hexstr=tx_dict['data']),
        )
        transaction.value = self.value
        transaction.token = self.token
        transaction.recipient_address = self.recipient_address
        return transaction

    def find_redeem_transaction(self):
        if self.network.filtering_supported:
            tx_details = self.network.find_transaction_details_in_redeem_event(
                block_number=self.block_number,
                recipient_address=self.recipient_address,
                secret_hash=self.secret_hash
            )
            if not tx_details:
                return

            return tx_details.get('transaction_hash')

        try:
            if self.is_token_contract:
                return self.network.find_redeem_token_transaction(
                    recipient_address=self.recipient_address,
                    token_address=self.token_address,
                    value=self.value_base_units,
                )
            return self.network.find_redeem_transaction(
                recipient_address=self.recipient_address,
                contract_address=self.contract_address,
                value=self.value_base_units,
            )
        except NotImplementedError:
            raise ValueError(
                f'Unable to find redeem transaction, {self.network.default_symbol} network is not supported.'
            )

    def find_secret(self):
        try:
            tx_details = self.network.find_transaction_details_in_redeem_event(
                block_number=self.block_number,
                recipient_address=self.recipient_address,
                secret_hash=self.secret_hash
            )
            if not tx_details:
                return

            return tx_details.get('secret')

        except NotImplementedError:
            raise ValueError(
                f'Unable to find secret, {self.network.default_symbol} network is not supported.'
            )

    def refund(self):
        if self.balance == 0:
            raise ValueError("Balance of this contract is 0.")
        contract = self.contract

        if self.locktime > datetime.utcnow():
            locktime_string = self.locktime.strftime('%Y-%m-%d %H:%M:%S')
            logger.warning(f"This contract is still valid! It can't be refunded until {locktime_string} UTC.")
            raise RuntimeError(f"This contract is still valid! It can't be refunded until {locktime_string} UTC.")

        refund_func = contract.functions.refund(self.secret_hash, self.recipient_address)
        tx_dict = {
            'nonce': self.network.web3.eth.getTransactionCount(self.refund_address),
            'value': 0,
            'gas': ETH_REFUND_GAS_LIMIT,
        }

        tx_dict = refund_func.buildTransaction(tx_dict)

        transaction = EthereumTokenTransaction(network=self.network)
        transaction.tx = Transaction(
            nonce=tx_dict['nonce'],
            gasprice=tx_dict['gasPrice'],
            startgas=tx_dict['gas'],
            to=tx_dict['to'],
            value=tx_dict['value'],
            data=Web3.toBytes(hexstr=tx_dict['data']),
        )
        transaction.value = self.value
        transaction.token = self.token
        transaction.recipient_address = self.refund_address
        logger.debug('Transaction refunded')
        return transaction

    def show_details(self):
        details = {
            'contract_address': self.contract_address,
            'confirmations': self.confirmations,
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.refund_address,
            'secret_hash': self.secret_hash,
            'transaction_address': self.tx_dict['hash'].hex(),
            'transaction_link': self.network.get_transaction_url(self.tx_dict['hash'].hex()),
            'value': self.value,
            'value_text': f'{self.value:.18f} {self.symbol}',
            'balance': self.balance,
        }
        if self.token:
            details['value_text'] = self.token.get_value_text(self.value)
            details['token_address'] = self.token_address
        return details
