from random import shuffle
import socket
from time import sleep, time
from typing import Optional

import bitcoin
from bitcoin import SelectParams
from bitcoin.base58 import Base58ChecksumError, InvalidBase58Error
from bitcoin.core import CTransaction, b2lx, b2x, script, x
from bitcoin.core.serialize import Hash, SerializationError, SerializationTruncationError
from bitcoin.messages import (
    MSG_TX,
    MsgSerializable,
    msg_getdata,
    msg_inv,
    msg_ping,
    msg_pong,
    msg_reject,
    msg_tx,
    msg_verack,
    msg_version,
)
from bitcoin.net import CInv
from bitcoin.wallet import CBitcoinAddress, CBitcoinAddressError

from clove.constants import (
    CLOVE_API_URL,
    NODE_COMMUNICATION_TIMEOUT,
    REJECT_TIMEOUT,
    TRANSACTION_BROADCASTING_MAX_ATTEMPTS,
)
from clove.exceptions import (
    ConnectionProblem,
    ImpossibleDeserialization,
    TransactionRejected,
    UnexpectedResponseFromNode,
)
from clove.network.base import BaseNetwork
from clove.network.bitcoin.contract import BitcoinContract
from clove.network.bitcoin.transaction import BitcoinAtomicSwapTransaction
from clove.network.bitcoin.wallet import BitcoinWallet
from clove.utils.bitcoin import auto_switch_params
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger
from clove.utils.network import generate_params_object


class BitcoinBaseNetwork(BaseNetwork):

    name = None
    '''Network name'''
    symbols = ()
    '''Tuple with network symbols'''
    seeds = ()
    '''Tuple with seed nodes addresses'''
    nodes = ()
    '''Tuple with nodes addresses or IPs'''
    port = None
    '''Port number used by network nodes'''
    connection = None
    '''Connection object'''
    protocol_version = None
    '''Protocol version number used by network nodes'''
    blacklist_nodes = {}
    '''List of dead nodes'''
    message_start = b''
    '''Message prefix'''
    base58_prefixes = {}
    '''Dictionary of different prefixes'''
    bitcoin_based = True
    '''Flag for bitcoin-based networks'''

    @classmethod
    def switch_params(cls):
        '''
        Method for changing network parameteres.

        Note:
            This method is used by the `auto_switch_params` decorator.
        '''
        if cls.name == 'bitcoin':
            SelectParams('mainnet')
        elif cls.name == 'test-bitcoin':
            SelectParams('testnet')
        else:
            SelectParams(
                name=cls.name,
                generic_params_object=generate_params_object(
                    name=cls.name,
                    message_start=cls.message_start,
                    base58_prefixes=cls.base58_prefixes,
                )
            )

    def publish(self, raw_transaction: str) -> Optional[str]:
        '''
        Method for publishing transactions.

        Args:
            raw_transaction (str): hex string containing signed transaction

        Returns:
            str, None: transaction address or None if transaction wasn't published

        Example:
            >>> raw_transaction = '010000000184a38a4e8743964249665fb241fbd3...35b'
            >>> network.publish(raw_transaction)
            70eefae0106b787e592e12914e4040efd8181dd299fa314d8f66da6a95cd1cfe
        '''
        for attempt in range(1, TRANSACTION_BROADCASTING_MAX_ATTEMPTS + 1):
            transaction_address = self.broadcast_transaction(raw_transaction)

            if transaction_address is None:
                logger.warning('Transaction broadcast attempt no. %s failed. Retrying...', attempt)
                continue

            logger.info('Transaction broadcast is successful. End of broadcasting process.')
            return transaction_address

        logger.warning(
            '%s attempts to broadcast transaction failed. Broadcasting process terminates!',
            TRANSACTION_BROADCASTING_MAX_ATTEMPTS
        )

    @staticmethod
    def get_nodes(seed: str) -> list:
        '''
        Extracting nodes from seed node.

        Args:
            seed (str): seed node address

        Returns:
            list: list of IPs of network nodes

        Example:
            >>> network.get_nodes('seed.testnet.bitcoin.sprovoost.nl')
            ['46.101.230.222',
             '47.97.79.7',
             '159.89.205.190',
             '163.44.175.226',
             '13.57.215.93',
             '18.191.17.25',
             '46.4.61.78',
             '104.248.185.143',
             '149.28.176.234',
             '71.13.92.62',
             '114.215.66.15',
             '178.128.244.253',
             '46.23.46.139',
             '54.37.192.136',
             '167.114.64.228',
             '159.89.128.32',
             '144.76.136.19',
             '18.212.60.14',
             '54.149.194.238',
             '52.53.159.115',
             '18.218.226.83']
        '''
        logger.debug('Getting nodes from seed node %s', seed)
        try:
            hostname, alias, nodes = socket.gethostbyname_ex(seed)
        except (socket.herror, socket.gaierror):
            return []
        logger.debug('Got %s nodes', len(nodes))
        return nodes

    @auto_switch_params()
    def capture_messages(self, expected_message_types: list, timeout: int=20, buf_size: int=1024,
                         ignore_empty: bool=False) -> list:
        '''
        Method for receiving messages from network nodes.

        Args:
            expected_message_types (list): list of message types to search for
            timeout (int): timeout for waiting for messages
            buf_size (int): buffer size that is going to be used for receiving messages
            ignore_empty (bool): flag for ignoring errors if the message that we're looking for wasn't found.
                Eg. this flag can be set to True when looking for reject messages because the absence of the
                reject message is not an error.

        Returns:
            list, None: list of received messages or None if none or not all expected message types were found

        Example:
            >>> from bitcoin.messages import msg_verack, msg_version
            >>> network.capture_messages([msg_version, msg_verack])
        '''
        deadline = time() + timeout
        found = []
        partial_message = None

        while expected_message_types and time() < deadline:

            try:
                received_data = self.connection.recv(buf_size)
                if partial_message:
                    received_data = partial_message + received_data
            except socket.timeout:
                continue

            if not received_data:
                sleep(0.1)
                continue

            for raw_message in self.split_message(received_data):

                try:
                    message = MsgSerializable.from_bytes(raw_message)
                except (SerializationError, SerializationTruncationError, ValueError):
                    partial_message = raw_message
                    continue

                partial_message = None
                if not message:
                    # unknown message type, skipping
                    continue

                msg_type = type(message)

                if msg_type is msg_ping:
                    logger.debug('Got ping, sending pong.')
                    self.send_pong(message)
                elif msg_type is msg_version:
                    logger.debug('Saving version')
                    self.protocol_version = message

                if msg_type in expected_message_types:
                    found.append(message)
                    expected_message_types.remove(msg_type)
                    logger.debug('Found %s, %s more to catch', msg_type.command.upper(), len(expected_message_types))

        if not expected_message_types:
            return found

        if not ignore_empty:
            logger.error('Not all messages could be captured')

    @auto_switch_params()
    def create_connection(self, node: str, timeout=2) -> Optional[socket.socket]:
        '''
        Establish connection to a given node.

        Args:
            node (str): node domain or IP address
            timeout (int): number of seconds to wait before raising timeout

        Returns:
            socket.socket: socket connection

        Example:
            >>> network.create_connection('104.248.185.143')
            <socket.socket fd=11, family=AddressFamily.AF_INET, type=2049, proto=6, laddr=('10.93.5.21', 36086), raddr=('104.248.185.143', 18333)>  # noqa: E501
        '''
        try:
            self.connection = socket.create_connection(
                address=(node, self.port),
                timeout=timeout
            )
        except (socket.timeout, ConnectionRefusedError, OSError):
            logger.debug('[%s] Could not establish connection to this node', node)
            return

        logger.debug('[%s] Connection established, sending version packet', node)
        if self.send_version():
            return self.connection

    @auto_switch_params()
    def connect(self) -> Optional[str]:
        '''
        Connects to some node from the network.

        Returns:
            str, None: node IP address or domain, None if doesn't connect to any node

        Example:
            >>> network.connect()
            '198.251.83.19'
            >>> network.connection
            <socket.socket fd=12, family=AddressFamily.AF_INET, type=2049, proto=6, laddr=('10.93.5.21', 54300), raddr=('198.251.83.19', 18333)>  # noqa: E501
        '''
        if self.connection and self.send_ping():
            # already connected
            return self.get_current_node()

        if self.nodes:
            # fake seed node to enter the seed nodes loop
            self.seeds = (None, )

        random_seeds = list(self.seeds)
        shuffle(random_seeds)

        for seed in random_seeds:

            if seed is None:
                # get hardcoded nodes
                nodes = self.nodes
            else:
                # get nodes from seed node
                nodes = self.get_nodes(seed)

            nodes = self.filter_blacklisted_nodes(nodes)

            for node in nodes:

                if not self.create_connection(node):
                    self.terminate(node)
                    continue

                messages = self.capture_messages([msg_version, msg_verack])
                if not messages:
                    logger.debug('[%s] Failed to get version or version acknowledge message from node', node)
                    self.terminate(node)
                    continue

                logger.debug('[%s] Got version, sending version acknowledge message', node)

                if not self.send_verack():
                    self.terminate(node)
                    continue

                return node

    def filter_blacklisted_nodes(self, nodes: list, max_tries_number=3) -> list:
        '''
        Filtering out dead nodes.

        Args:
            nodes (list): list of nodes to filter
            max_tries_number (int): maximum number of attempts to connect to a node (above this value node
                is being filtered out)

        Returns:
            list: list of nodes without dead nodes
        '''
        return sorted(
            [node for node in nodes if self.blacklist_nodes.get(node, 0) <= max_tries_number],
            key=lambda node: self.blacklist_nodes.get(node, 0)
        )

    def terminate(self, node: str=None):
        '''
        Closing connection to a given node and increasing number of failed connection attempts to this node.

        Args:
            node (str): node's IP address or domain. If the node was not given then this method will just
                close the existing connection.

        Returns:
            None
        '''
        if node:
            self.update_blacklist(node)
        if self.connection:
            self.connection.close()
            self.connection = None

    def update_blacklist(self, node):
        '''
        Increasing number of failed connection attempts to a give node.

        Args:
            node (str): node's IP address or domain

        Returns:
            None
        '''
        try:
            self.blacklist_nodes[node] += 1
        except KeyError:
            logger.warning('Unable to update  blacklist')
            self.blacklist_nodes[node] = 1

    @auto_switch_params()
    def version_packet(self) -> bitcoin.messages.msg_version:
        '''
        Creating version package for a current network.

        Returns:
            bitcoin.messages.msg_version
        '''
        packet = msg_version(170002)
        packet.addrFrom.ip, packet.addrFrom.port = self.connection.getsockname()
        packet.addrTo.ip, packet.addrTo.port = self.connection.getpeername()
        return packet

    @classmethod
    @auto_switch_params()
    def split_message(cls, received_data: bytes) -> list:
        '''
        Splits received data based on start message prefix.

        Args:
            received_data (bytes): portion of received data

        Returns:
            list: list of messages that were found
        '''
        return [
            bitcoin.params.MESSAGE_START + m for m in received_data.split(bitcoin.params.MESSAGE_START) if m
        ]

    @auto_switch_params()
    def send_message(self, msg: object, timeout: int=2) -> bool:
        '''
        Sends given message to the connected node.

        Args:
            msg (obj): bitcoin message object eg bitcoin.messages.msg_version or bitcoin.messages.msg_tx
            timeout (int): timeout for communication with connected node

        Returns:
            bool: True if the message was sent, False otherwise.

        Example:
            >>> from bitcoin.messages import msg_ping
            >>> network.send_message(msg_ping())
            True
        '''
        try:
            self.connection.settimeout(timeout)
            self.connection.send(msg.to_bytes())
        except (socket.timeout, ConnectionRefusedError, OSError) as e:
            logger.debug('Failed to send %s message', msg.command.decode())
            logger.debug(e)
            return False
        return True

    @auto_switch_params()
    def send_ping(self, timeout: int=1) -> bool:
        '''
        Sends ping message and tries to capture pong message.

        Args:
            timeout (int): timeout for communication with connected node

        Returns:
            bool: True if the message was sent, False otherwise.

        Example:
            >>> network.send_ping()
            True
        '''
        if not self.send_message(msg_ping(), timeout):
            return False
        if self.capture_messages([msg_pong, ]):
            return True
        return False

    @auto_switch_params()
    def send_pong(self, ping: msg_ping, timeout: int=1) -> bool:
        '''
        Sends pong message in response to ping message.

        Args:
            ping (bitcoin.messages.msg_ping): ping message that where received
            timeout (int): timeout for communication with connected node

        Returns:
            bool: True if the message was sent, False otherwise.

        Example:
            >>> network.send_pong(ping_message)
            True
        '''
        return self.send_message(
            msg_pong(self.protocol_version.nVersion, ping.nonce), timeout
        )

    @auto_switch_params()
    def send_verack(self, timeout: int=2) -> bool:
        '''
        Sending version acknowledge message.

        Args:
            timeout (int): timeout for communication with connected node

        Returns:
            bool: True if the message was sent, False otherwise.

        Example:
            >>> network.send_verack()
            True
        '''
        return self.send_message(
            msg_verack(self.protocol_version.nVersion), timeout
        )

    def send_version(self, timeout: int=2) -> bool:
        '''
        Sending version message.

        Args:
            timeout (int): timeout for communication with connected node

        Returns:
            bool: True if the message was sent, False otherwise.

        Example:
            >>> network.send_version()
            True
        '''
        return self.send_message(
            self.version_packet(), timeout
        )

    @auto_switch_params()
    def broadcast_transaction(self, raw_transaction: str) -> Optional[str]:
        '''
        Sends given transaction to connected node.

        Args:
            raw_transaction (str): hex string containing signed transaction

        Returns:
            str, None: transaction address if transaction was sent, None otherwise.
        '''
        deserialized_transaction = self.deserialize_raw_transaction(raw_transaction)
        serialized_transaction = deserialized_transaction.serialize()

        get_data = self.send_inventory(serialized_transaction)
        if not get_data:
            logger.debug(
                ConnectionProblem('Clove could not get connected with any of the nodes for too long.')
            )
            self.reset_connection()
            return

        node = self.get_current_node()

        if all(el.hash != Hash(serialized_transaction) for el in get_data.inv):
            logger.debug(UnexpectedResponseFromNode('Node did not ask for our transaction', node))
            self.reset_connection()
            return

        message = msg_tx()
        message.tx = deserialized_transaction

        if not self.send_message(message, 20):
            return

        logger.info('[%s] Looking for reject message.', node)
        messages = self.capture_messages([msg_reject, ], timeout=REJECT_TIMEOUT, buf_size=8192, ignore_empty=True)
        if messages:
            logger.debug(TransactionRejected(messages[0], node))
            self.reset_connection()
            return
        logger.info('[%s] Reject message not found.', node)

        transaction_address = b2lx(deserialized_transaction.GetHash())
        logger.info('[%s] Transaction %s has just been sent.', node, transaction_address)
        return transaction_address

    @auto_switch_params()
    def send_inventory(self, serialized_transaction) -> Optional[msg_getdata]:
        '''
        Sends inventory message with given serialized transaction to connected node.

        Returns:
            msg_getdata, None: get data request or None if something went wrong

        Note:
            This method is used by `broadcast_transaction` to inform connected node about existence
            of the new transaction.
        '''
        message = msg_inv()
        inventory = CInv()
        inventory.type = MSG_TX
        hash_transaction = Hash(serialized_transaction)
        inventory.hash = hash_transaction
        message.inv.append(inventory)

        timeout = time() + NODE_COMMUNICATION_TIMEOUT

        while time() < timeout:
            node = self.connect()
            if node is None:
                self.reset_connection()
                continue

            if not self.send_message(message):
                self.terminate(node)
                continue

            messages = self.capture_messages([msg_getdata, ])
            if not messages:
                self.terminate(node)
                continue

            logger.info('[%s] Node responded correctly.', node)
            return messages[0]

    def reset_connection(self):
        '''Disconnection from node if connected and clearing the blacklisted nodes.'''
        if self.connection:
            self.connection.close()
            self.connection = None
        self.blacklist_nodes = {}

    @classmethod
    @auto_switch_params()
    def get_new_wallet(cls) -> BitcoinWallet:
        '''
        Generates a new wallet.

        Example:
            >>> wallet = network.get_new_wallet()
            >>> wallet.address
            'mrkLKxgzfQk4dgFrfaoVYjeTkXxCfKyz1q'
        '''
        return cls.get_wallet()

    @classmethod
    def get_current_fee_per_kb(cls) -> Optional[float]:
        """
        Getting current network fee from Clove API

        Returns:
            float, None: current fee per kb or None if something went wrong

        Example:
            >>> network.get_current_fee_per_kb()
            0.01006814
        """

        network = cls.symbols[0].upper()
        if cls.testnet:
            network += '-TESTNET'
        resp = clove_req_json(f'{CLOVE_API_URL}/fee/{network}')

        if not resp:
            logger.debug('Could not get current fee for %s network', network)
            return

        return resp['fee']

    def get_current_node(self) -> Optional[str]:
        '''
        Getting address of connected node.

        Returns:
            str, None: IP for connected node or None if there is no connection established.

        Example:
            >>> network.get_current_node()
            '157.97.106.250'
        '''
        if self.connection:
            return self.connection.getpeername()[0]

    @auto_switch_params()
    def atomic_swap(
        self,
        sender_address: str,
        recipient_address: str,
        value: float,
        solvable_utxo: list=None,
        secret_hash: str=None,
    ) -> Optional[BitcoinAtomicSwapTransaction]:
        '''
        Creates atomic swap unsigned transaction object.

        Args:
            sender_address (str): wallet address of the sender
            recipient_address (str): wallet address of the recipient
            value (float): amount to swap
            solvable_utxo (list): optional list of UTXO objects. If None then it will try to find UTXO automatically
                by using the `get_utxo` method.
            secret_hash (str): optional secret hash to be used in transaction. If None then the new hash
                will be generated.

        Returns:
            BitcoinAtomicSwapTransaction, None: unsigned Atomic Swap transaction object or None if something went wrong

        Example:
            >>> from clove.network import BitcoinTestNet
            >>> network = BitcoinTestNet()
            >>> network.atomic_swap('msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM', 'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1', 2.4)
            <clove.network.bitcoin.transaction.BitcoinAtomicSwapTransaction at 0x7f989439d630>
        '''
        if not solvable_utxo:
            solvable_utxo = self.get_utxo(sender_address, value)
            if not solvable_utxo:
                logger.error(f'Cannot get UTXO for address {sender_address}')
                return
        transaction = BitcoinAtomicSwapTransaction(
            self, sender_address, recipient_address, value, solvable_utxo, secret_hash
        )
        transaction.create_unsigned_transaction()
        return transaction

    @auto_switch_params()
    def audit_contract(
        self,
        contract: str,
        raw_transaction: Optional[str]=None,
        transaction_address: Optional[str]=None,
    ) -> BitcoinContract:
        '''
        Getting details about an Atomic Swap contract.

        Args:
            contract (str): contract definition (hex string)
            raw_transaction (str): hex string with raw transaction
            transaction_address (str): hex string with transaction address which created an Atomic Swap

        Returns:
            BitcoinContract: contract object

        Example:
            >>> from clove.network import Litecoin
            >>> network = Litecoin()
            >>> network.audit_contract(
                contract='63a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',  # noqa: E501
                transaction_address='09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa'
            )
            <clove.network.bitcoin.contract.BitcoinContract at 0x7f98870db978>
        '''
        return BitcoinContract(self, contract, raw_transaction, transaction_address)

    @classmethod
    @auto_switch_params()
    def get_wallet(cls, private_key: str=None, encrypted_private_key: bytes=None, password: str=None) ->BitcoinWallet:
        '''
        Returns wallet object.

        Args:
            private_key (str): hex string with wallet's secret key
            encrypted_private_key (bytes): private key encrypted with password
            password (str): password for decrypting an encrypted private key

        Returns:
            BitcoinWallet: wallet object

        Example:
            >>> from clove.network import BitcoinTestNet
            >>> network = BitcoinTestNet()
            >>> wallet = network.get_wallet('cV8FDJu3JhLED2D7q5L7FwLCus69TajYGEnTWEbNqhzzV9WxMBE7')
            >>> wallet.address
            'mtUXc6UJTiwb5FdoEJ2hzR8R1yUrcj3hcn'

        Note:
            If private_key has not been provided then a new wallet will be generated just like via `get_new_wallet()`.
        '''
        return BitcoinWallet(private_key, encrypted_private_key, password)

    @classmethod
    def extract_secret(cls, raw_transaction: str=None, scriptsig: str=None) -> str:
        '''
        Extracting secret from Alice redeem transaction (first redeem in the Atomic Swao).

        Args:
            raw_transaction (str): raw transaction to extract secret from
            scriptSig (str): value of the scriptSig field from the first vin

        Returns:
            str: transaction secret

        Raises:
            ValueError: if something goes wrong

        Example:
            >>> from clove.network import Litecoin
            >>> network = Litecoin()
            >>> network.extract_secret(raw_transaction='0100000001aa25fd5f63cb41d6ee7dd495256046b4c3f17d4540a1b258a06bfefac30da60900000000fdff0047304402201c8869d359b5599ecffd51a96f0a8799392c98c4e15242762ba455e37b1f5d6302203f2974e9afc8d641f9363167df48e5a845a8deba1381bf5a1b549ac04718a1ac01410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf420c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9514c5163a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac00000000015a7b0100000000001976a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac00000000')  # noqa: E501
            'c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9'

            >>> network.extract_secret(scriptsig='0c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9514c5163a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20')  # noqa: E501
            'c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9'
        '''
        if not raw_transaction and not scriptsig:
            raise ValueError('raw_transaction or scriptsig have to be provided.')

        if raw_transaction:
            tx = cls.deserialize_raw_transaction(raw_transaction)

            if not tx.vin:
                raise ValueError('Given transaction has no inputs.')

            secret_tx_in = tx.vin[0]
            script_ops = list(secret_tx_in.scriptSig)
        else:
            script_ops = list(script.CScript.fromhex(scriptsig))

        if script_ops[-2] == 1:
            return b2x(script_ops[-3])

        raise ValueError('Unable to extract secret.')

    @classmethod
    @auto_switch_params()
    def is_valid_address(cls, address: str) -> bool:
        '''
        Checks if wallet address is valid for this network.

        Args:
            address (str): wallet address to check

        Returns:
            bool: True if address is valued, False otherwise

        Example:
            >>> from clove.network import Bitcoin
            >>> network = Bitcoin()
            >>> network.is_valid_address('13iNsKgMfVJQaYVFqp5ojuudxKkVCMtkoa')
            True
            >>> network.is_valid_address('msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM')
            False
        '''
        try:
            CBitcoinAddress(address)
        except (CBitcoinAddressError, Base58ChecksumError, InvalidBase58Error):
            return False

        return True

    @staticmethod
    def deserialize_raw_transaction(raw_transaction: str) -> CTransaction:
        '''
        Checking if transaction can be deserialized (is not corrupted).

        Args:
            raw_transaction (str): transaction to check

        Returns:
            CTransaction: transaction object

        Raises:
            ImpossibleDeserialization: when transaction is corrupted

        Example:
            >>> from clove.network import Litecoin
            >>> network = Litecoin()
            >>> network.deserialize_raw_transaction('0100000001aa25fd5f63cb41d6ee7dd495256046b4c3f17d4540a1b258a06bfefac30da60900000000fdff0047304402201c8869d359b5599ecffd51a96f0a8799392c98c4e15242762ba455e37b1f5d6302203f2974e9afc8d641f9363167df48e5a845a8deba1381bf5a1b549ac04718a1ac01410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf420c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9514c5163a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac00000000015a7b0100000000001976a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac00000000')  # noqa: E501
            CTransaction((CTxIn(COutPoint(lx('09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa'), 0), CScript([x('304402201c8869d359b5599ecffd51a96f0a8799392c98c4e15242762ba455e37b1f5d6302203f2974e9afc8d641f9363167df48e5a845a8deba1381bf5a1b549ac04718a1ac01'), x('0459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4'), x('c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9'), 1, x('63a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac')]), 0x0),), (CTxOut(0.00097114*COIN, CScript([OP_DUP, OP_HASH160, x('85c0522f6e23beb11cc3d066cd20ed732648a4e6'), OP_EQUALVERIFY, OP_CHECKSIG])),), 0, 1, CTxWitness())  # noqa: E501
        '''
        try:
            return CTransaction.deserialize(x(raw_transaction))
        except Exception:
            raise ImpossibleDeserialization()


class NoAPI(object):
    '''Empty class for networks that does not have block explorer with API.'''

    API = False

    @classmethod
    def get_latest_block(cls):
        raise NotImplementedError

    @staticmethod
    def get_transaction(tx_address: str) -> dict:
        raise NotImplementedError

    @classmethod
    def get_utxo(cls, address, amount):
        raise NotImplementedError

    @classmethod
    def extract_secret_from_redeem_transaction(cls, contract_address: str) -> Optional[str]:
        raise NotImplementedError

    @staticmethod
    def get_balance(wallet_address: str) -> float:
        raise NotImplementedError
