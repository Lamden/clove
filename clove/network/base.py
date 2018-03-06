import socket
from time import sleep, time
from typing import Optional

import bitcoin
from bitcoin import SelectParams
from bitcoin.core import CMutableTransaction, b2lx
from bitcoin.core.serialize import Hash, SerializationError, SerializationTruncationError
from bitcoin.messages import (
    MSG_TX, MsgSerializable, msg_getdata, msg_inv, msg_ping, msg_pong, msg_reject, msg_tx, msg_verack, msg_version
)
from bitcoin.net import CInv

from clove.constants import API_SUPPORTED_NETWORKS, NODE_COMMUNICATION_TIMEOUT
from clove.exceptions import ConnectionProblem, TransactionRejected, UnexpectedResponseFromNode
from clove.utils.external_source import get_fee_from_blockcypher, get_fee_from_last_transactions, get_utxo
from clove.utils.logging import logger
from clove.utils.network import generate_params_object


def auto_switch_params(args_index: int = 0):
    def wrap(f):
        def wrapped(*args, **kwargs):
            if 'network' in kwargs:
                kwargs['network'].switch_params()
            else:
                args[args_index].switch_params()
            return f(*args, **kwargs)
        return wrapped
    return wrap


class BaseNetwork(object):
    name = None
    symbols = ()
    seeds = ()
    port = None
    connection = None
    protocol_version = None
    blacklist_nodes = {}
    networks = {}
    test_networks = {}
    message_start = b''
    base58_prefixes = {}

    @classmethod
    def switch_params(cls):
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

    @property
    def default_symbol(self):
        if self.symbols:
            return self.symbols[0]

    @classmethod
    def is_test_network(cls):
        return cls.name and cls.name.startswith('test-')

    @classmethod
    def get_network_class_by_symbol(cls, symbol):
        symbol_mapping = cls.get_symbol_mapping()

        symbol = symbol.upper()
        if symbol not in symbol_mapping:
            raise RuntimeError(f'{symbol} network is not supported.')

        return symbol_mapping[symbol]

    @classmethod
    def get_symbol_mapping(cls):
        if not cls.networks:
            cls.set_symbol_mapping()

        if cls.is_test_network():
            return cls.test_networks
        return cls.networks

    @classmethod
    def set_symbol_mapping(cls):
        from clove.network import __all__
        cls.networks = cls.create_symbol_mapping(__all__)
        cls.test_networks = cls.create_symbol_mapping(__all__, testnet=True)

    @staticmethod
    def create_symbol_mapping(networks, testnet=False):
        return {
            symbol.upper(): network
            for network in networks
            for symbol in network.symbols
            if network.is_test_network() == testnet
        }

    @staticmethod
    def get_nodes(seed) -> list:
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
    def create_connection(self, node, timeout=2):
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
    def connect(self) -> str:

        if self.connection and self.send_ping():
            # already connected
            return self.get_current_node()

        for seed in self.seeds:
            nodes = self.filter_blacklisted_nodes(self.get_nodes(seed))

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

    def filter_blacklisted_nodes(self, nodes, max_tries_number=3):
        return sorted(
            [node for node in nodes if self.blacklist_nodes.get(node, 0) <= max_tries_number],
            key=lambda node: self.blacklist_nodes.get(node, 0)
        )

    def terminate(self, node=None):
        if node:
            self.update_blacklist(node)
        if self.connection:
            self.connection.close()
            self.connection = None

    def update_blacklist(self, node):
        try:
            self.blacklist_nodes[node] += 1
        except KeyError:
            self.blacklist_nodes[node] = 1

    @auto_switch_params()
    def version_packet(self):
        packet = msg_version(170002)
        packet.addrFrom.ip, packet.addrFrom.port = self.connection.getsockname()
        packet.addrTo.ip, packet.addrTo.port = self.connection.getpeername()
        return packet

    @classmethod
    @auto_switch_params()
    def split_message(cls, received_data: bytes) -> list:
        return [
            bitcoin.params.MESSAGE_START + m for m in received_data.split(bitcoin.params.MESSAGE_START) if m
        ]

    @auto_switch_params()
    def send_message(self, msg: object, timeout: int=2) -> bool:
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
        if not self.send_message(msg_ping(), timeout):
            return False
        if self.capture_messages([msg_pong, ]):
            return True
        return False

    @auto_switch_params()
    def send_pong(self, ping, timeout: int=1) -> bool:
        return self.send_message(
            msg_pong(self.protocol_version.nVersion, ping.nonce), timeout
        )

    @auto_switch_params()
    def send_verack(self, timeout: int=2) -> bool:
        return self.send_message(
            msg_verack(self.protocol_version.nVersion), timeout
        )

    def send_version(self, timeout: int=2) -> bool:
        return self.send_message(
            self.version_packet(), timeout
        )

    @auto_switch_params()
    def broadcast_transaction(self, transaction: CMutableTransaction):
        serialized_transaction = transaction.serialize()

        get_data = self.send_inventory(serialized_transaction)
        if not get_data:
            logger.debug(
                ConnectionProblem('Clove could not get connected with any of the nodes for too long.')
            )
            return self.reset_connection()

        node = self.get_current_node()

        if all(el.hash != Hash(serialized_transaction) for el in get_data.inv):
            logger.debug(UnexpectedResponseFromNode('Node did not ask for our transaction', node))
            return self.reset_connection()

        message = msg_tx()
        message.tx = transaction

        if not self.send_message(message, 20):
            return

        logger.info('[%s] Looking for reject message.', node)
        messages = self.capture_messages([msg_reject, ], timeout=5, buf_size=8192, ignore_empty=True)
        if messages:
            logger.debug(TransactionRejected(messages[0], node))
            return self.reset_connection()
        logger.info('[%s] Reject message not found.', node)

        transaction_hash = b2lx(transaction.GetHash())
        logger.info('[%s] Transaction %s has just been sent.', node, transaction_hash)
        return transaction_hash

    @auto_switch_params()
    def send_inventory(self, serialized_transaction) -> msg_getdata:
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
        if self.connection:
            self.connection.close()
            self.connection = None
        self.blacklist_nodes = {}

    @staticmethod
    def get_wallet():
        raise NotImplementedError

    @classmethod
    @auto_switch_params()
    def get_new_wallet(cls):
        return cls.get_wallet()

    @classmethod
    def get_current_fee_per_kb(cls) -> Optional[float]:
        """Returns current fee based on last transactions."""

        if cls.is_test_network() and cls.name != 'test-bitcoin':
            raise NotImplementedError

        network = cls.symbols[0].lower()
        if network in ('btc', 'ltc', 'doge', 'dash'):
            return get_fee_from_blockcypher(network, testnet=cls.is_test_network())

        if network not in API_SUPPORTED_NETWORKS:
            raise NotImplementedError

        return get_fee_from_last_transactions(network)

    def get_current_node(self):
        if self.connection:
            return self.connection.getpeername()[0]

    @classmethod
    def get_utxo(cls, address, amount):
        if cls.is_test_network() and cls.name != 'test-bitcoin':
            raise NotImplementedError

        network = cls.symbols[0].lower()
        if network == 'doge' or cls.name == 'test-bitcoin':
            return get_utxo(network, address, amount, use_blockcypher=True, testnet=cls.is_test_network())

        if network not in API_SUPPORTED_NETWORKS:
            raise NotImplementedError

        return get_utxo(network, address, amount)
