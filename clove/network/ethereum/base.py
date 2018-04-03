import os
from typing import Optional, Union

from eth_abi import decode_abi
from ethereum.transactions import Transaction
import rlp
from web3 import HTTPProvider, Web3
from web3.utils.abi import get_abi_input_types
from web3.utils.contracts import find_matching_fn_abi
from web3.utils.datastructures import AttributeDict

from clove.network.base import BaseNetwork
from clove.network.ethereum.contract import EthereumContract
from clove.network.ethereum.transaction import EthereumAtomicSwapTransaction
from clove.network.ethereum_based import Token
from clove.network.ethereum_based.mainnet_tokens import tokens


class EthereumBaseNetwork(BaseNetwork):
    """
    Class with all the necessary ETH network information and transaction building.
    """
    name = None
    symbols = ()
    infura_network = None
    ethereum_based = True
    contract_address = None

    def __init__(self):

        self.web3 = Web3(HTTPProvider(self.infura_endpoint))

        # Method IDs for transaction building. Built on the fly for developer reference (keeping away from magics)
        self.initiate = self.method_id('initiate(uint256,bytes20,address)')
        self.redeem = self.method_id('redeem(bytes32)')
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

    @staticmethod
    def extract_method_id(tx_input: str):
        return tx_input[2:10]

    def get_method_name(self, method_id):
        return {
            self.initiate: 'initiate',
            self.redeem: 'redeem',
            self.refund: 'refund',
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

        token = None
        if token_address:
            token = self.get_token_by_address(token_address)
            if not token:
                raise ValueError('Unknown token')

        transaction = EthereumAtomicSwapTransaction(
            token or self,
            sender_address,
            recipient_address,
            value,
            secret_hash,
            gas_price,
            gas_limit,
        )
        return transaction

    @staticmethod
    def sign(transaction: Transaction, private_key: str) -> Transaction:
        transaction.sign(private_key)
        return transaction

    def get_transaction(self, tx_address: str) -> AttributeDict:
        return self.web3.eth.getTransaction(tx_address)

    def audit_contract(self, tx_address: str) -> EthereumContract:
        tx_dict = self.get_transaction(tx_address)
        return EthereumContract(self, tx_dict)

    def extract_secret_from_redeem_transaction(self, tx_address: str) -> str:
        tx_dict = self.get_transaction(tx_address)
        method_id = self.extract_method_id(tx_dict['input'])
        if method_id != self.redeem:
            raise ValueError('Not a redeem transaction.')
        method_name = self.get_method_name(method_id)
        input_types = get_abi_input_types(find_matching_fn_abi(self.abi, fn_identifier=method_name))
        input_values = decode_abi(input_types, Web3.toBytes(hexstr=tx_dict['input'][10:]))
        return input_values[0].hex()

    @staticmethod
    def get_token_by_attribute(name: str, value: str) -> Optional[Token]:
        for token in tokens:
            if getattr(token, name).lower() == value.lower():
                return token

    def get_token_by_address(self, address: str):
        from clove.network.ethereum.token import EthereumToken

        token = self.get_token_by_attribute('address', address)
        if not token:
            return
        return EthereumToken.from_namedtuple(token)

    @classmethod
    def get_token_by_symbol(cls, symbol: str):
        from clove.network.ethereum.token import EthereumToken

        token = cls.get_token_by_attribute('symbol', symbol)
        if not token:
            return
        return EthereumToken.from_namedtuple(token)

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
