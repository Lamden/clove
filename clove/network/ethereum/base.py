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
    '''
    Class with all the necessary ETH network information and transaction building.
    '''
    API = True
    '''This value tells us that a given network have a block explorer API support.'''
    name = None
    '''Network name'''
    symbols = ()
    '''Tuple with network symbols'''
    web3_provider_address = None
    '''Address to a web3 provider'''
    ethereum_based = True
    '''Flag for ethereum-based networks'''
    contract_address = None
    '''Placeholder for a contract address'''
    tokens = []
    '''Placeholder for a list of tokens'''
    blockexplorer_tx = None
    '''Template string for the transaction address'''
    filtering_supported = False
    '''Support for filtering events'''

    abi = ETHEREUM_CONTRACT_ABI
    '''Application Binary Interface definition for Ethereum Atomic Swap contract.'''

    def __init__(self):

        self.web3 = Web3(HTTPProvider(self.web3_provider_address))

        # Method IDs for transaction building. Built on the fly for developer reference (keeping away from magics)
        self.initiate = self.method_id('initiate(uint256,bytes20,address,address,bool,uint256)')
        self.redeem = self.method_id('redeem(bytes32)')
        self.refund = self.method_id('refund(bytes20, address)')

    @staticmethod
    def method_id(method: str) -> str:
        '''
        Returns Atomic Swap methods identifiers.

        Args:
            method (str): method name with arguments

        Returns:
            str: method identifier

        Example:
            >>> from clove.network import Ethereum
            >>> network = Ethereum()
            >>> network.method_id('redeem(bytes32)')
            'eda1122c'
        '''
        return Web3.sha3(text=method)[0:4].hex()

    @staticmethod
    def extract_method_id(tx_input: str) -> str:
        '''
        Extract Atomic Swap method identifier from transaction input (hash string).

        Args:
            tx_inpit: hash string with transaction input

        Returns:
            str: method identifier

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.extract_method_id('0x7337c993000000000000000000000000000000000000000000000000000000005bd1e24b6603102c4aad175d1d719326d32127d55593f986000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a90920000000000000000000000004fd13283a6b9e26c4833d7b9ee7557f1d008371d0000000000000000000000000000000000000000000000000000000000000001000000000000000000000000000000000000000000000000002386f26fc10000')  # noqa: E501
            '7337c993'
        '''
        return tx_input[2:10]

    def get_method_name(self, method_id: str) -> str:
        '''
        Returning Atomic Swap method name based on method identifier.

        Args:
            method_id (str): method identifier

        Returns:
            str: method name

        Raises:
            UnsupportedTransactionType: if method identifier is not recognized

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_method_name('7337c993')
            'initiate'
        '''
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
    def value_from_base_units(value: int) -> Decimal:
        '''
        Converting value from base units.

        Args:
            value (int): value in base units (Wei)

        Returns:
            Decimal: value in main coins (Ethereum)

        Example:
            >>> from clove.network import Ethereum
            >>> network = Ethereum()
            >>> network.value_from_base_units(10000000000000)
            Decimal('0.00001')
        '''
        return Web3.fromWei(value, 'ether')

    @staticmethod
    def value_to_base_units(value: float) -> int:
        '''
        Converting value to base units.

        Args:
            value (int): value in main coins (Ethereum)

        Returns:
            float: value in base units (Wei)

        Example:
            >>> from clove.network import Ethereum
            >>> network = Ethereum()
            >>> network.value_to_base_units(0.00000001)
            10000000000
        '''
        return Web3.toWei(value, 'ether')

    @staticmethod
    def unify_address(address: str) -> str:
        '''
        Returns Ethereum address with checksum.

        Args:
            str: Ethereum address

        Returns:
            str: address with checksum

        Raises:
            AssertionError: if the address length is incorrect

        Example:
            >>> from clove.network import Ethereum
            >>> network = Ethereum()
            >>> network.unify_address('0x999f348959e611f1e9eab2927c21e88e48e6ef45')
            '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
        '''
        assert len(address) in (40, 42), 'Provided address is not properly formatted.'
        if len(address) == 40:
            address = '0x' + address
        int(address, 16)
        return Web3.toChecksumAddress(address)

    @staticmethod
    def is_valid_address(adddress: str) -> bool:
        '''
        Checking if given address is valid (with checksum or not).

        Args:
            str: Ethereum address

        Returns:
            bool: True if address is valid, False otherwise

        Example:
            >>> from clove.network import Ethereum
            >>> network = Ethereum()
            >>> network.is_valid_address('foobar')
            False
            >>> network.is_valid_address('0x999f348959e611f1e9eab2927c21e88e48e6ef45')
            True
        '''
        return Web3.isAddress(adddress)

    def atomic_swap(
        self,
        sender_address: str,
        recipient_address: str,
        value: Union[str, Decimal],
        secret_hash: str=None,
        token_address: str=None,
    ) -> EthereumAtomicSwapTransaction:
        '''
        Return EthereumAtomicSwapTransaction object, which initiate and build transaction between sender and recipient.

        Args:
            sender_address (str): wallet address of the sender
            recipient_address (str): wallet address of the recipient
            value (str, Decimal): amount to swap
            secret_hash (str): optional secret hash to be used in transaction. If None then the new hash
                will be generated.
            token_address: address of the ERC20 token contract to swap

        Returns:
            EthereumAtomicSwapTransaction: atomic swap unsigned transaction for Ethereum

        Raises:
            ValueError: if you use an incorrect token address

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.atomic_swap('0x999F348959E611F1E9eab2927c21E88E48e6Ef45', '0xd867f293Ba129629a9f9355fa285B8D3711a9092', '0.05')  # noqa: E501
            <clove.network.ethereum.transaction.EthereumAtomicSwapTransaction at 0x7f286d16dba8>
        '''

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
        '''
        Create unsigned token approve transaction.

        Args:
            sender_address (str): wallet address of the sender
            value (str, Decimal): amount to swap
            token_address: address of the ERC20 token contract to swap

        Returns:
            EthereumTokenApprovalTransaction: unsigned token approve transaction

        Raises:
            ValueError: if you use an incorrect token address

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.approve_token('0x999F348959E611F1E9eab2927c21E88E48e6Ef45', '0.05', '0x53E546387A0d054e7FF127923254c0a679DA6DBf')  # noqa: E501
            <clove.network.ethereum.transaction.EthereumTokenApprovalTransaction at 0x7f286d14bc50>
        '''
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
        '''
        Signing the transaction.

        Args:
            transaction (Transaction): Ethereum unsigned transaction object
            private_key (str): private key

        Returns:
            Transaction: Ethereum signed transaction object
        '''
        transaction.sign(private_key)
        logger.info('Transaction signed')
        return transaction

    def get_transaction(self, tx_address: str) -> AttributeDict:
        '''
        Getting transaction details.

        Args:
            tx_address (str): transaction address

        Returns:
            dict, None: dictionary with transaction details or None if transaction doesn't exist

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_transaction('0x9e41847c3cc780e4cb59902cf55657f0ee92642d9dee4145e090cbf206d4748f')
            AttributeDict({'blockHash': HexBytes('0x676df82b6cc2dcf34311bc21c5989452a5ef88c2ddf356991db15e1ee5ede159'),
             'blockNumber': 9181891,
             'chainId': None,
             'condition': None,
             'creates': None,
             'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
             'gas': 100000,
             'gasPrice': 1000000000,
             'hash': HexBytes('0x9e41847c3cc780e4cb59902cf55657f0ee92642d9dee4145e090cbf206d4748f'),
             'input': '0xeda1122cb2eefaadbbefeb9d9467092b612464db7c6724f71b5c1d70c85853845728f0e9',
             'nonce': 499,
             'publicKey': HexBytes('0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adcb150e5216213bc301f3a6b71a178c81ddd34a361d696c8cb03970590d4f'),  # noqa: E501
             'r': HexBytes('0xb5c8d879d9f85e6454f69cdf1c16ac2342999608d0366fa495b51ec61d33b9b7'),
             'raw': HexBytes('0xf88a8201f3843b9aca00830186a094ce07ab9477bc20790b88b398a2a9e0f626c7d26380a4eda1122cb2eefaadbbefeb9d9467092b612464db7c6724f71b5c1d70c85853845728f0e91ca0b5c8d879d9f85e6454f69cdf1c16ac2342999608d0366fa495b51ec61d33b9b7a01c35cc6de96f61543d92c21c572407481c05a3509af57fa3979d30258571b05a'),  # noqa: E501
             's': HexBytes('0x1c35cc6de96f61543d92c21c572407481c05a3509af57fa3979d30258571b05a'),
             'standardV': 1,
             'to': '0xce07aB9477BC20790B88B398A2A9e0F626c7D263',
             'transactionIndex': 2,
             'v': 28,
             'value': 0})
        '''
        return self.web3.eth.getTransaction(tx_address)

    def audit_contract(self, tx_address: str) -> EthereumContract:
        '''
        Getting details about an Atomic Swap contract.

        Args:
            transaction_address (str): hex string with transaction address which created an Atomic Swap

        Returns:
            EthereumContract: contract object

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.audit_contract('0xfe4bcc1b522923ca6f8dc2721134c7d8636b34737aeafb2d6d0868d73e226891')
            <clove.network.ethereum.contract.EthereumContract at 0x7f7b3fec3e80>
        '''
        tx_dict = self.get_transaction(tx_address)
        if not tx_dict:
            logger.info(f'Cannot audit contract, no such transaction: {tx_address} ({self.name})')
            return
        return EthereumContract(self, tx_dict)

    def extract_secret_from_redeem_transaction(self, tx_address: str) -> str:
        '''
        Extracting secret from redeem transaction.

        Args:
            tx_address (str): address of the redeem transaction

        Returns:
            str,: Secret string

        Raises:
            ValueError: When given transaction was not a redeem type transaction

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.extract_secret_from_redeem_transaction('0x9e41847c3cc780e4cb59902cf55657f0ee92642d9dee4145e090cbf206d4748f')  # noqa: E501
            b2eefaadbbefeb9d9467092b612464db7c6724f71b5c1d70c85853845728f0e9
        '''
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
        '''
        Get a known token (from clove) by provided attribute and its value.

        Args:
            name (str): attribute name
            value (str): attribute value

        Returns:
            Token, None: Ethereum Token namedtuple or None if there is no matching token

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_token_by_attribute('symbol', 'PGT')
            Token(name='PrettyGoodToken', symbol='PGT', address='0x2c76B98079Bb5520FF4BDBC1bf5012AC3E87ddF6', decimals=18)  # noqa: E501
        '''
        for token in cls.tokens:
            if getattr(token, name).lower() == value.lower():
                return token

    def get_token_from_token_contract(self, token_address: str) -> Optional[Token]:
        '''
        Getting information from token contract (remote)

        Args:
            token_address (str): address of the token contract

        Returns:
            Token, None: Ethereum Token namedtuple or None if there is something goes wrong

        Raises:
            RuntimeError: if name or symbol of the token is not defined.

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_token_from_token_contract('0x2c76B98079Bb5520FF4BDBC1bf5012AC3E87ddF6')
            Token(name='PrettyGoodToken', symbol='PGT', address='0x2c76B98079Bb5520FF4BDBC1bf5012AC3E87ddF6', decimals=18)  # noqa: E501
        '''
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

    def get_token_by_address(self, address: str) -> Optional[EthToken]:
        '''
        Get token by its address.

        Args:
            address (str): token address

        Returns:
            EthToken, None: Ethereum Token namedtuple

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_token_by_address('0x2c76B98079Bb5520FF4BDBC1bf5012AC3E87ddF6')
            <clove.network.ethereum.token.EthToken at 0x7f7b3fed1eb8>
        '''
        token = self.get_token_by_attribute('address', address) or self.get_token_from_token_contract(address)
        if not token:
            logger.warning(f'No token found for address {address}')
            return
        return EthToken.from_namedtuple(token)

    @classmethod
    def get_token_by_symbol(cls, symbol: str) -> Optional[EthToken]:
        '''
        Get a known token (from clove) by its symbol.

        Args:
            symbol (str): token symbol

        Returns:
            EthToken, None: Ethereum Token namedtuple or None if there is no matching token

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_token_by_symbol('PGT')
            <clove.network.ethereum.token.EthToken at 0x7f7b3fdffe48>
        '''
        token = cls.get_token_by_attribute('symbol', symbol)
        if not token:
            logger.warning(f'No token found for symbol {symbol}')
            return
        return EthToken.from_namedtuple(token)

    @staticmethod
    def deserialize_raw_transaction(raw_transaction: str) -> Transaction:
        '''
        Deserializing raw transaction and returning Transaction object

        Args:
            raw_transaction (str): raw transaction hex string

        Returns:
            `ethereum.transactions.Transaction`: Ethereum transaction object

        Raises:
            ImpossibleDeserialization: if the raw transaction was not deserializable

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> transaction = network.deserialize_raw_transaction('0xf8f28201f4843b9aca008302251694ce07ab9477bc20790b88b398a2a9e0f626c7d26387b1a2bc2ec50000b8c47337c993000000000000000000000000000000000000000000000000000000005bd564819d3e84874c199ca4656d434060ec1a393750ab74000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a9092000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000808080')  # noqa: E501
            <Transaction(821b)>
        '''
        try:
            transaction = rlp.hex_decode(raw_transaction, Transaction)
            logger.debug('Deserialization succeed')
        except (ValueError, RLPException):
            logger.warning(f'Deserialization with {raw_transaction} failed')
            raise ImpossibleDeserialization()

        transaction._cached_rlp = None
        transaction.make_mutable()

        return transaction

    @staticmethod
    def get_raw_transaction(transaction: Transaction) -> str:
        '''
        Get raw_transaction by encoding Transaction object

        Args:
            transaction (`ethereum.transactions.Transaction`): Ethereum transaction object

        Returns:
            str: raw transaction hex string

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> transaction = network.deserialize_raw_transaction('0xf8f28201f4843b9aca008302251694ce07ab9477bc20790b88b398a2a9e0f626c7d26387b1a2bc2ec50000b8c47337c993000000000000000000000000000000000000000000000000000000005bd564819d3e84874c199ca4656d434060ec1a393750ab74000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a9092000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000808080')  # noqa: E501
            >>> network.get_raw_transaction(transaction)
            '0xf8f28201f4843b9aca008302251694ce07ab9477bc20790b88b398a2a9e0f626c7d26387b1a2bc2ec50000b8c47337c993000000000000000000000000000000000000000000000000000000005bd564819d3e84874c199ca4656d434060ec1a393750ab74000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a9092000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000808080'  # noqa: E501
        '''
        return Web3.toHex(rlp.encode(transaction))

    @classmethod
    def sign_raw_transaction(cls, raw_transaction: str, private_key: str) -> str:
        '''
        Method to sign raw transactions.

        Args:
            raw_transaction (str): raw transaction hex string
            private_key (str): private key hex string

        Returns:
            str: signed transaction hex string

        Raises:
            ValueError: if given private key is invalid

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> raw_transaction = '0xf8f28201f4843b9aca008302251694ce07ab9477bc20790b88b398a2a9e0f626c7d26387b1a2bc2ec50000b8c47337c993000000000000000000000000000000000000000000000000000000005bd564819d3e84874c199ca4656d434060ec1a393750ab74000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a9092000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000808080'  # noqa: E501
            >>> network.sign_raw_transaction(raw_transaction, MY_PRIVATE_KEY)
            '0xf901318201f4843b9aca008302251694ce07ab9477bc20790b88b398a2a9e0f626c7d26387b1a2bc2ec50000b8c47337c993000000000000000000000000000000000000000000000000000000005bd564819d3e84874c199ca4656d434060ec1a393750ab74000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a90920000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ca0d1c5b984ef2629eeb7c96f48a645566b2caf4130b0f3d7060ad5225946eee9e99f9928c5dfe868b45efbb9f8ae7d64d6162591c78961439c49e836947842e178'  # noqa: E501
        '''
        transaction = cls.deserialize_raw_transaction(raw_transaction)

        try:
            transaction.sign(private_key)
            logger.debug("Transaction signed")
        except Exception:
            logger.warning("Invalid private key. Transaction could not be signed.")
            raise ValueError('Invalid private key.')

        return cls.get_raw_transaction(transaction)

    def publish(self, transaction: Union[str, Transaction]) -> Optional[str]:
        '''
        Method to publish transaction

        Args:
            transaction (str, `ethereum.transactions.Transaction`): signed transaction

        Returns:
            str, None: transaction hash or None if something goes wrong

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> signed_transaction = '0xf901318201f4843b9aca008302251694ce07ab9477bc20790b88b398a2a9e0f626c7d26387b1a2bc2ec50000b8c47337c993000000000000000000000000000000000000000000000000000000005bd564819d3e84874c199ca4656d434060ec1a393750ab74000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a90920000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001ca0d1c5b984ef2629eeb7c96f48a645566b2caf4130b0f3d7060ad5225946eee9e99f9928c5dfe868b45efbb9f8ae7d64d6162591c78961439c49e836947842e178'  # noqa: E501
            >>> network.publish(signed_transaction)
            '0x4fd41289b816f6122e59a0759bd10441ead75d550562f4b3aad2fddc56eb3274'
        '''
        raw_transaction = transaction if isinstance(transaction, str) else self.get_raw_transaction(transaction)
        try:
            published_transaction = self.web3.eth.sendRawTransaction(raw_transaction).hex()
            logger.debug(f'Transaction {published_transaction} published successful')
            return published_transaction
        except ValueError:
            logger.warning(f'Unable to publish transaction {raw_transaction}')
            return

    @classmethod
    def get_wallet(cls, private_key=None) -> EthereumWallet:
        '''
        Returns Ethereum wallet object, which allows to keep address and private.

        Args:
            private_key (str, None): private key

        Returns:
            EthereumWallet: Ethereum wallet object

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> method.get_wallet(private_key=MY_PRIVATE_KEY)
            <clove.network.ethereum.wallet.EthereumWallet at 0x7f7b3febd518>
        '''
        return EthereumWallet(private_key)

    @classmethod
    def get_new_wallet(cls) -> EthereumWallet:
        '''
        Returns new Ethereum wallet object, which allows to keep address and private key.

        Returns:
            EthereumWallet: Ethereum wallet object

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> method.get_new_wallet()
            <clove.network.ethereum.wallet.EthereumWallet at 0x7f7b3fdff898>
        '''
        return cls.get_wallet()

    @property
    def get_latest_block(self):
        '''
        Returns the number of the latest block.

        Returns:
            int: number of the latest block

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_latest_block
            9188959
        '''
        return self.web3.eth.blockNumber

    def find_redeem_transaction(self, recipient_address: str, contract_address: str, value: int):
        '''Placeholder'''
        raise NotImplementedError

    def find_redeem_token_transaction(self, recipient_address: str, token_address: str, value: int):
        '''Placeholder'''
        raise NotImplementedError

    def find_transaction_details_in_redeem_event(
        self,
        recipient_address: str,
        secret_hash: str,
        block_number: int,
    ) -> Optional[dict]:
        '''
        Searching for transaction details of redeem transaction in Atomic Swap contract events.

        Args:
            recipient_address (str): recipient address
            secret_hash (str): hash of the secret
            block_number (int): number of the block from which filtering should be started

        Returns:
            dict, None: dictionary with secret and transaction hash, None if no redeem transaction where found

        Raises:
            NotImplementedError: if the network doesn't support event filtering
        '''
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
        """
        Returns transaction url for a given transaction hash in block explorer.

        Args:
            tx_hash (str): transaction hash

        Returns:
            str, None: Url to transaction, None if `blockexplorer_tx` was not set for this network.

        Example:
            >>> from clove.network import EthereumTestnet
            >>> network = EthereumTestnet()
            >>> network.get_transaction_url('0x9e41847c3cc780e4cb59902cf55657f0ee92642d9dee4145e090cbf206d4748f')
            'https://kovan.etherscan.io/tx/0x9e41847c3cc780e4cb59902cf55657f0ee92642d9dee4145e090cbf206d4748f'
        """
        if not cls.blockexplorer_tx:
            return
        return cls.blockexplorer_tx.format(tx_hash)
