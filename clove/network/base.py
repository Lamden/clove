import json
import socket
from time import sleep
from urllib.error import HTTPError, URLError
import urllib.request

from bitcoin import params
from bitcoin.core import COIN, SerializationTruncationError
from bitcoin.messages import MsgSerializable, msg_ping, msg_verack, msg_version


class BaseNetwork(object):
    name = None
    symbols = ()
    seeds = ()
    port = None
    connection = None
    protocol_version = None

    @property
    def default_symbol(self):
        if self.symbols:
            return self.symbols[0]

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
                nodes = self.get_nodes(seed)
                for node in nodes:
                    try:
                        self.connection = socket.create_connection(
                            address=(node, self.port),
                            timeout=timeout
                        )
                        self.connection.send(self.version_packet())
                        sleep(0.1)
                        self.protocol_version = MsgSerializable.from_bytes(
                            self.clean_message(self.connection.recv(1024), b'version')
                        )

                        self.connection.send(msg_verack().to_bytes())
                        sleep(0.1)
                        self.connection.recv(1024)

                    except (socket.timeout, ConnectionRefusedError, OSError):
                        continue
                    return

    def version_packet(self):
        packet = msg_version()
        packet.addrFrom.ip, packet.addrFrom.port = self.connection.getsockname()
        packet.addrTo.ip, packet.addrTo.port = self.connection.getpeername()
        return packet.to_bytes()

    @staticmethod
    def clean_message(message, command):
        messages = reversed(message.split(params.MESSAGE_START))
        message = next((message for message in messages if command in message), b'')
        return params.MESSAGE_START + message

    def ping(self):
        self.connect()
        self.connection.send(msg_ping().to_bytes())
        sleep(0.1)
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
        if symbol not in ('btc', 'ltc', 'doge', 'dash') or cls.name.startswith('test-'):
            raise NotImplementedError
        try:
            with urllib.request.urlopen(f'https://api.blockcypher.com/v1/{symbol}/main') as url:
                if url.status != 200:
                    return
                data = json.loads(url.read().decode())
                return data['high_fee_per_kb'] / COIN
        except (URLError, HTTPError):
            return
