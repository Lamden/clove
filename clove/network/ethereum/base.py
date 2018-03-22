from datetime import datetime, timedelta
import hashlib
import os
import secrets
from typing import Union

from ethereum.transactions import Transaction
import rlp
from web3 import HTTPProvider, Web3

from clove.network.base import BaseNetwork


class EthereumBaseNetwork(BaseNetwork):
    """
    Class with all the necessary ETH network information and transaction building.
    """
    name = None
    symbols = ()
    infura_network = None
    ethereum_based = True
    eth_swap_contract_address = None
    token_swap_contract_address = None

    # downloaded from 'Contract ABI' at etherscan.io
    eth_abi = [{
        'constant': False,
        'inputs': [{
            'name': '_hash',
            'type': 'bytes20'
        }],
        'name': 'refund',
        'outputs': [],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }, {
        'constant': False,
        'inputs': [{
            'name': '_expiration',
            'type': 'uint256'
        }, {
            'name': '_hash',
            'type': 'bytes20'
        }, {
            'name': '_participant',
            'type': 'address'
        }],
        'name': 'initiate',
        'outputs': [],
        'payable': True,
        'stateMutability': 'payable',
        'type': 'function'
    }, {
        'constant': False,
        'inputs': [{
            'name': '_secret',
            'type': 'bytes32'
        }],
        'name': 'redeem',
        'outputs': [],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }]

    token_abi = [{
        "constant": False,
        "inputs": [{
            "name": "_expiration",
            "type": "uint256"
        }, {
            "name": "_hash",
            "type": "bytes20"
        }, {
            "name": "_participant",
            "type": "address"
        }, {
            "name": "_token",
            "type": "address"
        }, {
            "name": "_value",
            "type": "uint256"
        }],
        "name": "initiate",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }, {
        "constant": False,
        "inputs": [{
            "name": "_hash",
            "type": "bytes20"
        }],
        "name": "refund",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }, {
        "constant": False,
        "inputs": [{
            "name": "_secret",
            "type": "bytes32"
        }],
        "name": "redeem",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }]

    def __init__(self):

        self.web3 = Web3(HTTPProvider(self.infura_endpoint))

        # Method IDs for transaction building. Built on the fly for developer reference (keeping away from magics)
        self.initiate = self.method_id('initiate(uint256,bytes20,address)')
        self.participate = self.method_id('participate(uint256,bytes20,address)')
        self.redeem = self.method_id('redeem(bytes32,bytes20)')
        self.refund = self.method_id('refund(bytes20)')
        self.swaps = self.method_id('swaps(bytes20)')

    @property
    def infura_endpoint(self) -> str:
        token = os.environ.get('INFURA_TOKEN')
        if not token:
            raise ValueError('INFURA_TOKEN environment variable was not set.')
        return f'https://{self.infura_network}.infura.io/{token}'

    @staticmethod
    def method_id(method) -> str:
        return Web3.sha3(method.encode('ascii'))[2:10]

    @staticmethod
    def generate_secret() -> bytes:
        return secrets.token_bytes(32)

    @staticmethod
    def unify_address(address):
        assert len(address) in (40, 42), 'Provided address is not properly formatted.'
        if len(address) == 40:
            address = '0x' + address
        int(address, 16)
        return address

    def atomic_swap(
        self,
        recipient_address: str,
        hours_to_expiration: int,
        secret: bytes=None,
        secret_hash: bytes=None,
    ) -> tuple:

        recipient_address = self.unify_address(recipient_address)

        if secret is not None and secret_hash is not None:
            raise ValueError('Provide secret or secret_hash argument, not both.')

        if secret:
            assert len(secret) == 32, 'Secret provided must be 32 bytes'
            try:
                secret.hex()
            except SyntaxError:
                raise ValueError('Incorrect value of secret argument')

        else:
            secret = self.generate_secret()

        if secret_hash:
            try:
                secret_hash.hex()
            except SyntaxError:
                raise ValueError('Incorrect value of secret_hash argument')
        else:
            h = hashlib.new('ripemd160')
            h.update(secret)
            secret_hash = h.digest()

        unix_time_until_expiration = int((datetime.now() + timedelta(hours=hours_to_expiration)).timestamp())

        return unix_time_until_expiration, secret_hash, recipient_address

    def initial_transaction(
        self,
        sender_address: str,
        recipient_address: str,
        value: float,
        gas_limit: int=None,
        gas_price: int=None,
        token_address: str=None,
    ) -> Transaction:

        payload = self.atomic_swap(recipient_address, hours_to_expiration=48)
        if token_address:
            contract_address = self.token_swap_contract_address
            abi = self.token_abi
        else:
            contract_address = self.eth_swap_contract_address
            abi = self.eth_abi

        contract = self.web3.eth.contract(address=contract_address, abi=abi)
        initiate_func = contract.functions.initiate(*payload)

        if gas_limit is None:
            gas_limit = initiate_func.estimateGas()

        tx_dict = {
            'nonce': self.web3.eth.getTransactionCount(sender_address),
            'from': sender_address,
            'gas': gas_limit,
            'value': value,
        }

        if gas_price:
            tx_dict['gasPrice'] = gas_price

        return initiate_func.buildTransaction(tx_dict)

    @staticmethod
    def sign(transaction: Transaction, private_key: str) -> Transaction:
        transaction.sign(private_key)
        return transaction

    @staticmethod
    def get_raw_transaction(transaction: Transaction) -> str:
        return Web3.toHex(rlp.encode(transaction))

    def broadcast_transaction(self, transaction: Union[str, Transaction]) -> bool:

        raw_transaction = transaction if isinstance(transaction, str) else self.get_raw_transaction(transaction)

        try:
            self.web3.eth.sendRawTransaction(raw_transaction)
        except ValueError:
            return False
        return True
