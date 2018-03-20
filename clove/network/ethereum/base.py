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
    abi = [{
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
        if len(address) == 42:
            address = address[2:]
        int(address, 16)
        return address

    def atomic_swap(
        self,
        recipient_address: str,
        hours_to_expiration: int,
        secret: bytes=None,
        secret_hash: bytes=None,
    ) -> bytes:

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
            method_id = self.participate
        else:
            h = hashlib.new('ripemd160')
            h.update(secret)
            secret_hash = h.digest().hex()
            method_id = self.initiate

        unix_time_until_expiration = int((datetime.now() + timedelta(hours=hours_to_expiration)).timestamp())
        expiration_arg = hex(unix_time_until_expiration)[2:].zfill(64)
        recipient_arg = recipient_address.zfill(64)
        secret_arg = secret_hash.ljust(64, '0')

        return Web3.toBytes(text=f'{method_id}{expiration_arg}{secret_arg}{recipient_arg}')

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
        if self.token_address:
            contract_address = self.token_swap_contract_address
        else:
            contract_address = self.eth_swap_contract_address

        contract = self.web3.eth.contract(address=contract_address, abi=self.abi)
        return contract.functions.initiate.buildTransaction(
            nonce=self.web3.eth.getTransactionCount(sender_address),
            gasprice=gas_price,
            to=recipient_address,
            startgas=gas_limit,
            data=payload,
            value=value,
        )

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
