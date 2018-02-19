import json
import logging
import socket
from urllib.error import HTTPError, URLError
import urllib.request

import bitcoin
from bitcoin import SelectParams
from bitcoin.core import COIN, CMutableTransaction, b2lx
from bitcoin.core.serialize import Hash, SerializationError, SerializationTruncationError
from bitcoin.messages import (
    MSG_TX, MsgSerializable, msg_getdata, msg_inv, msg_ping, msg_pong, msg_reject, msg_tx, msg_verack, msg_version
)
from bitcoin.net import CInv
import coloredlogs

from clove.network.exceptions import ConnectionProblem, TransactionRejected, UnexpectedResponseFromNode
from clove.utils.logging import log_inappropriate_response_messages
from clove.utils.network import generate_params_object, recvall

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

coloredlogs.install(logger=logger, level=logging.DEBUG)


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
    nodes = None
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

    def get_all_nodes(self) -> list:
        return [node for seed in self.seeds for node in self.get_nodes(seed)]

    @auto_switch_params()
    def connect(self, timeout=2):

        if self.nodes is None:
            self.nodes = self.get_all_nodes()

        if self.connection is None:
            nodes = self.filter_blacklisted_nodes(self.nodes)
            for node in nodes:
                self.update_blacklist(node)

                try:
                    self.connection = socket.create_connection(
                        address=(node, self.port),
                        timeout=timeout
                    )
                    logger.debug('[%s] Connection established, sending version packet', node)
                    self.connection.send(self.version_packet())
                    self.connection.settimeout(timeout)
                except (socket.timeout, ConnectionRefusedError, OSError) as e:
                    logger.debug('[%s] Could not establish connection to this node', node)
                    logger.exception(e)
                    self.terminate(node)

                messages = recvall(self.connection, 1024)

                try:
                    self.protocol_version = MsgSerializable.from_bytes(
                        self.clean_message(messages, b'version')
                    )
                except (socket.timeout, SerializationError, SerializationTruncationError) as e:
                    logger.debug('[%s] Failed to get version packet from node', node)
                    logger.exception(e)
                    self.terminate(node)
                    continue

                logger.debug('[%s] Got version, sending version acknowledge message', node)

                try:
                    self.connection.send(msg_verack(self.protocol_version.nVersion).to_bytes())
                    self.connection.settimeout(timeout)
                except (socket.timeout, ConnectionRefusedError, OSError) as e:
                    logger.debug('[%s] Failed to send version acknowledge message', node)
                    logger.exception(e)
                    self.terminate(node)
                    continue

                return

    def filter_blacklisted_nodes(self, nodes, max_tries_number=3):
        return sorted(
            [node for node in nodes if self.blacklist_nodes.get(node, 0) <= max_tries_number],
            key=lambda node: self.blacklist_nodes.get(node, 0)
        )

    def terminate(self, node=None, blacklist=False):
        if node and blacklist:
            self.update_blacklist(node)
        elif node:
            self.nodes.remove(node)
        if self.connection:
            self.connection.close()
            self.connection = None

    def update_blacklist(self, node):
        try:
            self.blacklist_nodes[node] += 1
        except KeyError:
            self.blacklist_nodes[node] = 1

    def version_packet(self):
        packet = msg_version(170002)
        packet.addrFrom.ip, packet.addrFrom.port = self.connection.getsockname()
        packet.addrTo.ip, packet.addrTo.port = self.connection.getpeername()
        return packet.to_bytes()

    @classmethod
    @auto_switch_params()
    def clean_message(cls, message: bytes, command: bytes) -> bytes:
        messages = message.split(bitcoin.params.MESSAGE_START)
        message = next((message for message in messages if command in message), b'')
        return bitcoin.params.MESSAGE_START + message

    @auto_switch_params()
    def ping(self):
        self.connect()
        self.connection.send(msg_ping().to_bytes())
        self.connection.settimeout(0.1)
        pong = None
        try:
            pong = MsgSerializable.from_bytes(self.clean_message(recvall(self.connection, 1024), b'pong'))
        except SerializationTruncationError:
            pass
        return pong

    @staticmethod
    def get_wallet():
        raise NotImplementedError

    @classmethod
    @auto_switch_params()
    def get_new_wallet(cls):
        return cls.get_wallet()

    @classmethod
    def get_current_fee_per_kb(cls) -> float:
        """Returns current high priority (1-2 blocks) fee estimates."""
        symbol = cls.symbols[0].lower()
        if symbol not in ('btc', 'ltc', 'doge', 'dash') or cls.is_test_network():
            raise NotImplementedError
        try:
            with urllib.request.urlopen(f'https://api.blockcypher.com/v1/{symbol}/main') as url:
                if url.status != 200:
                    return
                data = json.loads(url.read().decode())
                return data['high_fee_per_kb'] / COIN
        except (URLError, HTTPError):
            return

    @auto_switch_params()
    def broadcast_transaction(self, transaction: CMutableTransaction):
        serialized_transaction = transaction.serialize()
        got_data = self.set_inventory(serialized_transaction)
        transaction_hash = b2lx(transaction.GetHash())
        node = self.connection.getpeername()[0]

        if not got_data:
            return logger.exception(
                ConnectionProblem('Clove could not get connected with any of the nodes for too long.', node)
            )
        elif all(el.hash != Hash(serialized_transaction) for el in got_data.inv):
            return logger.exception(UnexpectedResponseFromNode('Unknown error', node))

        message = msg_tx()
        message.tx = transaction

        self.connection.sendall(message.to_bytes())
        self.connection.settimeout(20)

        try:
            responses = self.extract_all_responses(recvall(self.connection, 8192))
        except socket.timeout:
            logger.debug('[%s] Connection timeout. Node is not responding. Connection terminates.', node)
            return self.terminate()
        rejects = [
            f"{el.message.decode('ascii')} {el.reason.decode('ascii')}"
            for el in responses if isinstance(el, msg_reject)
        ]
        if rejects:
            return logger.exception(TransactionRejected('; '.join(rejects), node))

        logger.info('[%s] Transaction %s has just been sent.', node, transaction_hash)
        return transaction_hash

    @auto_switch_params()
    def set_inventory(self, serialized_transaction) -> msg_getdata:
        message = msg_inv()
        inventory = CInv()
        inventory.type = MSG_TX
        hash_transaction = Hash(serialized_transaction)
        inventory.hash = hash_transaction
        message.inv.append(inventory)

        while True:
            self.connect()
            if self.connection is None:
                self.blacklist_nodes = {}
                self.nodes = None
                continue

            node = self.connection.getpeername()[0]

            try:
                self.connection.sendall(message.to_bytes())
                self.connection.settimeout(2)
                messages = self.extract_all_responses(recvall(self.connection, 8192))
            except socket.timeout:
                self.terminate(node=node)
                continue

            message_getdata = next((message for message in messages if isinstance(message, msg_getdata)), None)
            message_ping = next((message for message in messages if isinstance(message, msg_ping)), None)

            if message_getdata:
                logger.info('[%s] Node responded correctly. Sending transaction...', node)
                return message_getdata
            elif message_ping:
                self.connection.send(msg_pong(self.protocol_version.nVersion, message_ping.nonce).to_bytes())
            else:
                log_inappropriate_response_messages(logger, messages, node)
                self.terminate(node=node, blacklist=True)

    @classmethod
    @auto_switch_params()
    def extract_all_responses(cls, buffer: bytes) -> list:
        prefix = bitcoin.params.MESSAGE_START
        messages = [prefix + message for message in buffer.split(prefix) if message]
        responses = []
        for message in messages:
            try:
                deserialized_msg = MsgSerializable.from_bytes(message)
                if deserialized_msg:
                    responses.append(deserialized_msg)
            except (SerializationTruncationError, SerializationError, ValueError) as e:
                logger.debug('Could not deserialize: %s', e)
        return responses
