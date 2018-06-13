from datetime import datetime, timedelta, timezone
from decimal import Decimal
from typing import Optional

from bitcoin.core import x
from ethereum.transactions import Transaction
import rlp
from web3 import Web3

from clove.constants import ETH_TOKEN_SWAP_GAS_LIMIT
from clove.utils.hashing import generate_secret_with_hash


class EthereumTransaction(object):
    '''Ethereum transaction object.'''

    def __init__(self, network):
        self.network = network
        self.tx = None
        self.value = None
        self.recipient_address = None

    @property
    def raw_transaction(self) -> str:
        '''Returns raw transaction serialized to hex.'''
        return Web3.toHex(rlp.encode(self.tx))

    def show_details(self) -> dict:
        '''Returns information about transaction.'''
        details = self.tx.to_dict()
        details['transaction_address'] = details.pop('hash')
        details['gas_limit'] = details.pop('startgas')
        details['transaction'] = self.raw_transaction

        if self.recipient_address:
            details['recipient_address'] = self.recipient_address

        value = self.value
        if not value:
            value = self.network.value_from_base_units(self.tx.value)
        details['value'] = value
        details['value_text'] = f'{value:.18f} {self.network.default_symbol}'
        return details

    def sign(self, private_key):
        return self.tx.sign(private_key)

    def publish(self) -> Optional[str]:
        return self.network.publish(self.tx)


class EthereumTokenTransaction(EthereumTransaction):
    '''Ethereum token transaction object.'''

    def __init__(self, network):
        super().__init__(network)

        self.token = None
        self.value = None
        self.value_base_units = None
        self.symbol = None

    def show_details(self) -> dict:
        '''Returns information about transaction.'''
        details = super().show_details()

        if self.token:
            details['value_text'] = self.token.get_value_text(self.value)
            details['value'] = self.value

        return details


class EthereumTokenApprovalTransaction(EthereumTokenTransaction):

    def __init__(
        self,
        network,
        sender_address: str,
        value: Decimal,
        token=None,
    ):
        super().__init__(network)

        self.sender_address = self.network.unify_address(sender_address)
        self.value = value
        self.token = token
        self.value_base_units = self.token.value_to_base_units(self.value)
        self.token_address = self.token.token_address
        self.symbol = self.token.symbol

        self.contract = self.network.web3.eth.contract(address=self.token_address, abi=self.token.approve_abi)

        approve_func = self.contract.functions.approve(
            self.token.contract_address,
            self.value_base_units,
        )

        tx_dict = {
            'nonce': self.network.web3.eth.getTransactionCount(self.sender_address),
            'from': self.sender_address,
        }

        tx_dict = approve_func.buildTransaction(tx_dict)

        self.gas_limit = approve_func.estimateGas({
            key: value for key, value in tx_dict.items() if key not in ('to', 'data')
        })

        self.tx = Transaction(
            nonce=tx_dict['nonce'],
            gasprice=tx_dict['gasPrice'],
            startgas=self.gas_limit,
            to=tx_dict['to'],
            value=tx_dict['value'],
            data=Web3.toBytes(hexstr=tx_dict['data']),
        )

    def show_details(self):
        details = super().show_details()
        details['contract_address'] = self.token.contract_address
        details['token_address'] = Web3.toChecksumAddress(details.pop('to'))
        details['sender_address'] = self.sender_address
        return details


class EthereumAtomicSwapTransaction(EthereumTokenTransaction):
    init_hours = 48
    participate_hours = 24

    def __init__(
        self,
        network,
        sender_address: str,
        recipient_address: str,
        value: Decimal,
        secret_hash: str=None,
        token=None,
    ):
        super().__init__(network)

        self.sender_address = network.unify_address(sender_address)
        self.recipient_address = network.unify_address(recipient_address)
        self.secret = None
        self.secret_hash = x(secret_hash) if secret_hash else None
        self.value = value
        self.token = token
        self.gas_limit = None
        self.contract = None
        self.locktime = None
        self.locktime_unix = None

        self.set_locktime()
        self.set_secrets()

        if self.token:
            self.token_address = self.token.token_address
            self.symbol = self.token.symbol
            self.contract_address = self.token.contract_address
            self.abi = self.token.abi
            self.value_base_units = self.token.value_to_base_units(self.value)
            self.set_token_contract()
        else:
            self.symbol = self.network.default_symbol
            self.contract_address = self.network.contract_address
            self.abi = self.network.abi
            self.value_base_units = self.network.value_to_base_units(self.value)
            self.set_contract()

    def set_secrets(self):
        if self.secret_hash:
            try:
                self.secret_hash.hex()
            except SyntaxError:
                raise ValueError('Incorrect value of secret_hash argument')
        else:
            self.secret, self.secret_hash = generate_secret_with_hash()

    def set_locktime(self):
        self.locktime = datetime.utcnow() + timedelta(hours=24 if self.secret_hash else 48)
        self.locktime_unix = int(self.locktime.replace(tzinfo=timezone.utc).timestamp())

    def set_contract(self):
        self.contract = self.network.web3.eth.contract(address=self.contract_address, abi=self.abi)

        initiate_func = self.contract.functions.initiate(
            self.locktime_unix,
            self.secret_hash,
            self.recipient_address,
        )

        tx_dict = {
            'nonce': self.network.web3.eth.getTransactionCount(self.sender_address),
            'from': self.sender_address,
            'value': self.value_base_units,
        }

        tx_dict = initiate_func.buildTransaction(tx_dict)

        self.gas_limit = initiate_func.estimateGas({
            key: value for key, value in tx_dict.items() if key not in ('to', 'data')
        })

        self.tx = Transaction(
            nonce=tx_dict['nonce'],
            gasprice=tx_dict['gasPrice'],
            startgas=self.gas_limit,
            to=tx_dict['to'],
            value=tx_dict['value'],
            data=Web3.toBytes(hexstr=tx_dict['data']),
        )

    def set_token_contract(self):
        self.contract = self.network.web3.eth.contract(address=self.contract_address, abi=self.abi)

        initiate_func = self.contract.functions.initiate(
            self.locktime_unix,
            self.secret_hash,
            self.recipient_address,
            self.token_address,
            self.value_base_units
        )

        tx_dict = {
            'nonce': self.network.web3.eth.getTransactionCount(self.sender_address),
            'from': self.sender_address,
            'value': 0,
            'gas': ETH_TOKEN_SWAP_GAS_LIMIT,
        }

        tx_dict = initiate_func.buildTransaction(tx_dict)

        self.tx = Transaction(
            nonce=tx_dict['nonce'],
            gasprice=tx_dict['gasPrice'],
            startgas=tx_dict['gas'],
            to=tx_dict['to'],
            value=tx_dict['value'],
            data=Web3.toBytes(hexstr=tx_dict['data']),
        )

    def show_details(self):
        details = super().show_details()
        details['secret'] = self.secret.hex() if self.secret else ''
        details['secret_hash'] = self.secret_hash.hex()
        details['locktime'] = self.locktime
        details['sender_address'] = self.sender_address
        details['recipient_address'] = self.recipient_address
        details['contract_address'] = self.contract_address
        details['refund_address'] = self.sender_address
        if self.token:
            details['token_address'] = self.token_address
        return details
