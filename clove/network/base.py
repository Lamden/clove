import json
import socket
from urllib.error import HTTPError, URLError
import urllib.request

from bitcoin.core import COIN, CMutableTransaction
from bitcoin.core.serialize import Hash, SerializationError, SerializationTruncationError
from bitcoin.messages import (
    MSG_TX, MsgSerializable, msg_getdata, msg_inv, msg_ping, msg_pong, msg_reject, msg_tx, msg_verack, msg_version
)
from bitcoin.net import CInv


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

    @property
    def default_symbol(self):
        if self.symbols:
            return self.symbols[0]

    @classmethod
    def is_test_network(cls):
        return cls.name.startswith('test-')

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
        try:
            hostname, alias, nodes = socket.gethostbyname_ex(seed)
        except (socket.herror, socket.gaierror):
            return []

        return nodes

    def connect(self, timeout=2):
        if self.connection is None:
            for seed in self.seeds:
                nodes = self.filter_blacklisted_nodes(self.get_nodes(seed))
                for node in nodes:
                    self.update_blacklist(node)
                    try:
                        self.connection = socket.create_connection(
                            address=(node, self.port),
                            timeout=timeout
                        )
                        self.connection.send(self.version_packet())
                        self.connection.settimeout(0.2)
                        try:
                            self.protocol_version = MsgSerializable.from_bytes(
                                self.clean_message(self.connection.recv(1024), b'version')
                            )
                        except SerializationTruncationError:
                            self.terminate(node)
                            continue

                        self.connection.send(msg_verack(self.protocol_version.nVersion).to_bytes())
                        self.connection.settimeout(0.2)
                        self.connection.recv(1024)

                    except (socket.timeout, ConnectionRefusedError, OSError):
                        continue
                    return

    def filter_blacklisted_nodes(self, nodes, max_tries_number=3):
        return [node for node in nodes if self.blacklist_nodes.get(node, 0) <= max_tries_number]

    def terminate(self, node=None):
        if node:
            self.update_blacklist(node)
        self.connection.close()
        self.connection = None

    def update_blacklist(self, node):
        try:
            self.blacklist_nodes[node] += 1
        except KeyError:
            self.blacklist_nodes[node] = 1

    def version_packet(self):
        packet = msg_version()
        packet.addrFrom.ip, packet.addrFrom.port = self.connection.getsockname()
        packet.addrTo.ip, packet.addrTo.port = self.connection.getpeername()
        return packet.to_bytes()

    @staticmethod
    def clean_message(message: bytes, command: bytes) -> bytes:
        from bitcoin import params
        messages = reversed(message.split(params.MESSAGE_START))
        message = next((message for message in messages if command in message), b'')
        return params.MESSAGE_START + message

    def ping(self):
        self.connect()
        self.connection.send(msg_ping().to_bytes())
        self.connection.settimeout(0.1)
        pong = None
        try:
            pong = MsgSerializable.from_bytes(self.clean_message(self.connection.recv(1024), b'pong'))
        except SerializationTruncationError:
            pass
        return pong

    @staticmethod
    def get_wallet():
        raise NotImplementedError

    def get_new_wallet(self):
        return self.get_wallet()

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

    def broadcast_transaction(self, transaction: CMutableTransaction):
        serialized_transaction = transaction.serialize()
        got_data = self.set_inventory(serialized_transaction)

        if got_data and any(el.hash == Hash(serialized_transaction) for el in got_data.inv):
            message = msg_tx()
            message.tx = transaction
            self.connection.sendall(message.to_bytes())
            self.connection.settimeout(120)

            responses = self.extract_all_the_responses(self.connection.recv(8192))
            if any(isinstance(response, msg_reject) for response in responses):
                NotImplementedError
            return responses

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
                break

            try:
                self.connection.sendall(message.to_bytes())
                self.connection.settimeout(2)
                messages = self.extract_all_the_responses(self.connection.recv(8192))
            except socket.timeout:
                self.terminate(node=self.connection.getpeername()[0])
                continue

            message_getdata = next((message for message in messages if isinstance(message, msg_getdata)), None)
            message_ping = next((message for message in messages if isinstance(message, msg_ping)), None)

            if message_getdata:
                return message_getdata
            elif message_ping:
                self.connection.send(msg_pong(self.protocol_version.nVersion, message_ping.nonce).to_bytes())
            else:
                self.terminate(node=self.connection.getpeername()[0])

    @staticmethod
    def extract_all_the_responses(buffer: bytes) -> list:
        from bitcoin import params
        prefix = params.MESSAGE_START
        messages = [prefix + message for message in buffer.split(prefix)]
        responses = []
        for message in messages:
            try:
                responses.append(MsgSerializable.from_bytes(message))
            except (SerializationTruncationError, SerializationError, ValueError):
                pass
        return responses
