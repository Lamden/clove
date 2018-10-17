from decimal import Decimal
from typing import Optional, Union

from eth_abi import decode_abi, encode_single
from ethereum.transactions import Transaction
import rlp
from rlp import RLPException
from web3 import HTTPProvider, Web3
from web3.contract import ConciseContract
from web3.exceptions import BadFunctionCallOutput
from web3.utils.abi import get_abi_input_types
from web3.utils.contracts import find_matching_fn_abi
from web3.utils.datastructures import AttributeDict

from clove.constants import ERC20_BASIC_ABI, ETH_FILTER_MAX_ATTEMPTS, ETHEREUM_CONTRACT_ABI
from clove.exceptions import ImpossibleDeserialization, UnsupportedTransactionType
from clove.network.base import BaseNetwork
from clove.network.ethereum.contract import EthereumContract
from clove.network.ethereum.token import EthToken
from clove.network.ethereum.transaction import EthereumAtomicSwapTransaction, EthereumTokenApprovalTransaction
from clove.network.ethereum.wallet import EthereumWallet
from clove.network.ethereum_based import Token
from clove.utils.logging import logger


class EthereumBaseNetwork(BaseNetwork):
    """
    Class with all the necessary ETH network information and transaction building.
    """
    API = True

    name = None
    symbols = ()
    web3_provider_address = None
    ethereum_based = True
    contract_address = None
    tokens = []
    blockexplorer_tx = None
    filtering_supported = False

    abi = ETHEREUM_CONTRACT_ABI

    def __init__(self):

        self.web3 = Web3(HTTPProvider(self.web3_provider_address))

        # Method IDs for transaction building. Built on the fly for developer reference (keeping away from magics)
        self.initiate = self.method_id('initiate(uint256,bytes20,address,address,bool,uint256)')
        self.redeem = self.method_id('redeem(bytes32)')
        self.refund = self.method_id('refund(bytes20, address)')

    @staticmethod
    def method_id(method) -> str:
        return Web3.sha3(text=method)[0:4].hex()

    @staticmethod
    def extract_method_id(tx_input: str):
        return tx_input[2:10]

    def get_method_name(self, method_id):
        try:
            return {
                self.initiate: 'initiate',
                self.redeem: 'redeem',
                self.refund: 'refund',
            }[method_id]
        except KeyError:
            logger.warning(f'Unrecognized method id {self.method_id}')
            raise UnsupportedTransactionType(f'Unrecognized method id {self.method_id}')

    @staticmethod
    def value_from_base_units(value: int):
        return Web3.fromWei(value, 'ether')

    @staticmethod
    def value_to_base_units(value: float):
        return Web3.toWei(value, 'ether')

    @staticmethod
    def unify_address(address):
        assert len(address) in (40, 42), 'Provided address is not properly formatted.'
        if len(address) == 40:
            address = '0x' + address
        int(address, 16)
        return Web3.toChecksumAddress(address)

    @staticmethod
    def is_valid_address(adddress: str) -> bool:
        return Web3.isAddress(adddress)

    def atomic_swap(
        self,
        sender_address: str,
        recipient_address: str,
        value: Union[str, Decimal],
        secret_hash: str=None,
        token_address: str=None,
    ) -> EthereumAtomicSwapTransaction:
        """ Return EthereumAtomicSwapTransaction object,
            which initiate and build transaction beetwen sender and recipient """

        if not isinstance(value, Decimal):
            value = Decimal(str(value))

        token = None
        if token_address:
            token = self.get_token_by_address(token_address)
            if not token:
                logger.warning('Unknown ethereum token')
                raise ValueError('Unknown token')

        transaction = EthereumAtomicSwapTransaction(
            self,
            sender_address,
            recipient_address,
            value,
            secret_hash,
            token,
        )
        return transaction

    def approve_token(
        self,
        sender_address: str,
        value: Union[str, Decimal],
        token_address: str=None,
    ) -> EthereumTokenApprovalTransaction:

        if not isinstance(value, Decimal):
            value = Decimal(str(value))

        token = None
        if token_address:
            token = self.get_token_by_address(token_address)
            if not token:
                logger.warning('Unknown ethereum token')
                raise ValueError('Unknown token')

        transaction = EthereumTokenApprovalTransaction(
            self,
            sender_address,
            value,
            token,
        )

        return transaction

    @staticmethod
    def sign(transaction: Transaction, private_key: str) -> Transaction:
        transaction.sign(private_key)
        logger.info('Transaction signed')
        return transaction

    def get_transaction(self, tx_address: str) -> AttributeDict:
        return self.web3.eth.getTransaction(tx_address)

    def audit_contract(self, tx_address: str) -> EthereumContract:
        tx_dict = self.get_transaction(tx_address)
        if not tx_dict:
            logger.info(f'Cannot audit contract, no such transaction: {tx_address} ({self.name})')
            return
        return EthereumContract(self, tx_dict)

    def extract_secret_from_redeem_transaction(self, tx_address: str) -> str:
        tx_dict = self.get_transaction(tx_address)
        method_id = self.extract_method_id(tx_dict['input'])
        if method_id != self.redeem:
            logger.debug('Not a redeem transaction.')
            raise ValueError('Not a redeem transaction.')
        method_name = self.get_method_name(method_id)
        input_types = get_abi_input_types(find_matching_fn_abi(self.abi, fn_identifier=method_name))
        input_values = decode_abi(input_types, Web3.toBytes(hexstr=tx_dict['input'][10:]))
        return input_values[0].hex()

    @classmethod
    def get_token_by_attribute(cls, name: str, value: str) -> Optional[Token]:
        """ Get a token by provided attribute and its value """
        for token in cls.tokens:
            if getattr(token, name).lower() == value.lower():
                return token

    def get_token_from_token_contract(self, token_address: str) -> Optional[Token]:
        """ Getting information from token contract and creating Token.
            Smart contract is taken based on provided address """
        token_address = self.unify_address(token_address)
        token_contract = self.web3.eth.contract(address=token_address, abi=ERC20_BASIC_ABI)
        concise = ConciseContract(token_contract)
        try:
            name = concise.name()
            symbol = concise.symbol()
            decimals = concise.decimals()
            if name == '' or symbol == '':
                raise RuntimeError('Unable to extract token details from token contract')
            logger.debug(f'Token get from contract with success')
        except (OverflowError, BadFunctionCallOutput):
            logger.warning(f'Unable to take token from address: {token_address}')
            return
        return Token(name, symbol, token_address, decimals)

    def get_token_by_address(self, address: str):
        token = self.get_token_by_attribute('address', address) or self.get_token_from_token_contract(address)
        if not token:
            logger.warning(f'No token found for address {address}')
            return
        return EthToken.from_namedtuple(token)

    @classmethod
    def get_token_by_symbol(cls, symbol: str):
        """  Get raw_transaction by encoding Transaction object token by provided symbol """
        token = cls.get_token_by_attribute('symbol', symbol)
        if not token:
            logger.warning(f'No token found for symbol {symbol}')
            return
        return EthToken.from_namedtuple(token)

    @staticmethod
    def get_raw_transaction(transaction: Transaction) -> str:
        """ Get raw_transaction by encoding Transaction object """
        return Web3.toHex(rlp.encode(transaction))

    @staticmethod
    def deserialize_raw_transaction(raw_transaction: str) -> Optional[Transaction]:
        """ Method to deserialize raw method.
        It's deserializing raw_transaction and returns Transaction object"""
        try:
            transaction = rlp.hex_decode(raw_transaction, Transaction)
            logger.debug('Deserialization succeed')
        except (ValueError, RLPException):
            logger.warning(f'Deserialization with {raw_transaction} failed')
            raise ImpossibleDeserialization()

        transaction._cached_rlp = None
        transaction.make_mutable()

        return transaction

    @classmethod
    def sign_raw_transaction(cls, raw_transaction: str, private_key: str) -> str:
        """ Method to sign raw transactions """
        transaction = cls.deserialize_raw_transaction(raw_transaction)

        try:
            transaction.sign(private_key)
            logger.debug("Transaction signed")
        except Exception:
            logger.warning("Invalid private key. Transaction could not be signed.")
            raise ValueError('Invalid private key.')

        return cls.get_raw_transaction(transaction)

    def publish(self, transaction: Union[str, Transaction]) -> Optional[str]:
        """ Method to publish transaction """
        raw_transaction = transaction if isinstance(transaction, str) else self.get_raw_transaction(transaction)
        try:
            published_transaction = self.web3.eth.sendRawTransaction(raw_transaction).hex()
            logger.debug(f'Transaction {published_transaction} published successful')
            return published_transaction
        except ValueError:
            logger.warning(f'Unable to publish transaction {raw_transaction}')
            return

    @classmethod
    def get_wallet(cls, private_key=None):
        """ Returns Ethereum wallter object, which allows to keep address and priv key """
        return EthereumWallet(private_key)

    @classmethod
    def get_new_wallet(cls):
        """ Returns new Ethereum wallter object, which allows to keep address and priv key """
        return cls.get_wallet()

    @property
    def get_latest_block(self):
        return self.web3.eth.blockNumber

    def find_redeem_transaction(self, recipient_address: str, contract_address: str, value: int):
        raise NotImplementedError

    def find_redeem_token_transaction(self, recipient_address: str, token_address: str, value: int):
        raise NotImplementedError

    def find_transaction_details_in_redeem_event(self, recipient_address: str, secret_hash: str, block_number: int):
        if not self.filtering_supported:
            raise NotImplementedError

        event_signature_hash = self.web3.sha3(text="RedeemSwap(address,bytes20,bytes32)").hex()
        filter_options = {
            'fromBlock': block_number,
            'address': self.contract_address,
            'topics': [
                event_signature_hash,
                '0x' + encode_single('address', recipient_address).hex(),
                '0x' + encode_single('bytes20', bytes.fromhex(secret_hash)).hex()
            ]
        }

        event_filter = self.web3.eth.filter(filter_options)

        for _ in range(ETH_FILTER_MAX_ATTEMPTS):
            events = event_filter.get_all_entries()
            if events:
                return {
                    'secret': events[0]['data'][2:],
                    'transaction_hash': events[0]['transactionHash'].hex()
                }

    @classmethod
    def get_transaction_url(cls, tx_hash: str) -> Optional[str]:
        if not cls.blockexplorer_tx:
            return
        return cls.blockexplorer_tx.format(tx_hash)
