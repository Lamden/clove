from datetime import datetime

from eth_abi import decode_abi
from web3 import Web3
from web3.utils.abi import get_abi_input_names, get_abi_input_types
from web3.utils.contracts import find_matching_fn_abi


class EthereumContract(object):

    def __init__(self, network, tx_dict):
        self.network = network
        self.tx_dict = tx_dict
        self.type = self.network.get_method_name(tx_dict['input'][2:10])

        input_types = get_abi_input_types(find_matching_fn_abi(self.abi, fn_identifier=self.type))
        input_names = get_abi_input_names(find_matching_fn_abi(self.abi, fn_identifier=self.type))
        input_values = decode_abi(input_types, Web3.toBytes(hexstr=self.tx_dict['input'][10:]))
        self.inputs = dict(zip(input_names, input_values))
        self.locktime = datetime.fromtimestamp(self.inputs['_expiration'])
        self.recipient_address = self.inputs['_participant']
        self.secret_hash = self.inputs['_hash'].hex()

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

    def redeem(self):
        pass

    def refund(self):
        pass

    def show_details(self):
        value_text = Web3.fromWei(self.tx_dict['value'], 'ether')
        return {
            'contract_address': self.tx_dict['to'],
            'transaction_address': self.tx_dict['hash'].hex(),
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.tx_dict['from'],
            'secret_hash': self.secret_hash,
            'value': self.tx_dict['value'],
            'value_text': f'{value_text:.18f} {self.network.default_symbol}',
        }
