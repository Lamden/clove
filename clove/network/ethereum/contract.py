from datetime import datetime

from eth_abi import decode_abi
from ethereum.transactions import Transaction
from web3 import Web3
from web3.utils.abi import get_abi_input_names, get_abi_input_types
from web3.utils.contracts import find_matching_fn_abi

from clove.constants import ETH_REDEEM_GAS_LIMIT
from clove.network.ethereum.transaction import EthereumTransaction


class EthereumContract(object):

    def __init__(self, network, tx_dict):

        self.network = network
        self.tx_dict = tx_dict
        self.method_id = self.network.extract_method_id(tx_dict['input'])
        self.type = self.network.get_method_name(self.method_id)

        if not self.is_initiate:
            raise ValueError('Not a contract transaction.')

        input_types = get_abi_input_types(find_matching_fn_abi(self.abi, fn_identifier=self.type))
        input_names = get_abi_input_names(find_matching_fn_abi(self.abi, fn_identifier=self.type))
        input_values = decode_abi(input_types, Web3.toBytes(hexstr=self.tx_dict['input'][10:]))
        self.inputs = dict(zip(input_names, input_values))

        self.locktime = datetime.utcfromtimestamp(self.inputs['_expiration'])
        self.recipient_address = Web3.toChecksumAddress(self.inputs['_participant'])
        self.secret_hash = self.inputs['_hash'].hex()

        self.value = self.tx_dict['value']
        self.contract_address = Web3.toChecksumAddress(self.tx_dict['to'])

    @property
    def is_eth_contract(self):
        return self.tx_dict['to'] == self.network.eth_swap_contract_address

    @property
    def is_initiate(self):
        return self.method_id == self.network.initiate

    @property
    def abi(self):
        if self.is_eth_contract:
            return self.network.eth_abi
        return self.network.token_abi

    def participate(
        self,
        symbol: str,
        sender_address: str,
        recipient_address: str,
        value: int,
        utxo: list=None,
        token_address: str=None,
    ):
        network = self.network.get_network_by_symbol(symbol)
        if network.ethereum_based:
            return network.atomic_swap(
                sender_address,
                recipient_address,
                value,
                self.secret_hash
            )
        return network.atomic_swap(
            sender_address,
            recipient_address,
            value,
            utxo,
            self.secret_hash,
        )

    def redeem(self, secret: str, gas_price: int=None) -> EthereumTransaction:
        contract = self.network.web3.eth.contract(address=self.contract_address, abi=self.abi)
        redeem_func = contract.functions.redeem(secret)
        tx_dict = {
            'nonce': self.network.web3.eth.getTransactionCount(self.recipient_address),
            'value': 0,
            'gas': ETH_REDEEM_GAS_LIMIT,
        }

        if gas_price:
            tx_dict['gasPrice'] = gas_price

        tx_dict = redeem_func.buildTransaction(tx_dict)

        transaction = EthereumTransaction(network=self.network)
        transaction.tx = Transaction(
            nonce=tx_dict['nonce'],
            gasprice=tx_dict['gasPrice'],
            startgas=tx_dict['gas'],
            to=tx_dict['to'],
            value=tx_dict['value'],
            data=Web3.toBytes(hexstr=tx_dict['data']),
        )
        return transaction

    def refund(self):
        pass

    def show_details(self):
        value_text = Web3.fromWei(self.tx_dict['value'], 'ether')
        return {
            'contract_address': self.contract_address,
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.tx_dict['from'],
            'secret_hash': self.secret_hash,
            'transaction_address': self.tx_dict['hash'].hex(),
            'value': self.tx_dict['value'],
            'value_text': f'{value_text:.18f} {self.network.default_symbol}',
        }
