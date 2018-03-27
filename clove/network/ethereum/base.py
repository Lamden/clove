import os
from typing import Union

from ethereum.transactions import Transaction
import rlp
from web3 import HTTPProvider, Web3

from clove.network.base import BaseNetwork
from clove.network.ethereum.contract import EthereumContract
from clove.network.ethereum.transaction import EthereumAtomicSwapTransaction


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

    @property
    def infura_endpoint(self) -> str:
        token = os.environ.get('INFURA_TOKEN')
        if not token:
            raise ValueError('INFURA_TOKEN environment variable was not set.')
        return f'https://{self.infura_network}.infura.io/{token}'

    @staticmethod
    def method_id(method) -> str:
        return Web3.sha3(text=method)[0:4].hex()

    def get_method_name(self, method_id):
        return {
            self.initiate: 'initiate',
            self.participate: 'participate',
            self.redeem: 'redeem',
            self.refund: 'refund',
            self.swaps: 'swaps',
        }[method_id]

    @staticmethod
    def unify_address(address):
        assert len(address) in (40, 42), 'Provided address is not properly formatted.'
        if len(address) == 40:
            address = '0x' + address
        int(address, 16)
        return address

    def atomic_swap(
        self,
        sender_address: str,
        recipient_address: str,
        value: float,
        secret_hash: bytes=None,
        token_address: str=None,
        gas_price: int=None,
        gas_limit: int=None,
    ) -> EthereumAtomicSwapTransaction:

        transaction = EthereumAtomicSwapTransaction(
            self,
            sender_address,
            recipient_address,
            value,
            secret_hash,
            token_address,
            gas_price,
            gas_limit,
        )
        return transaction

    @staticmethod
    def sign(transaction: Transaction, private_key: str) -> Transaction:
        transaction.sign(private_key)
        return transaction

    def audit_contract(self, tx_address: str) -> EthereumContract:
        tx_dict = self.web3.eth.getTransaction(tx_address)
        return EthereumContract(self, tx_dict)

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
