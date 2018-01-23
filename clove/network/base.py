from collections import namedtuple
import socket


class BaseNetwork(object):
    name = None
    symbols = ()
    seeds = ()
    port = None

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

    @classmethod
    def connect(cls, timeout=2):
        for seed in cls.seeds:
            nodes = cls.get_nodes(seed)
            for node in nodes:
                try:
                    connection = socket.create_connection(
                        address=(node, cls.port),
                        timeout=timeout
                    )
                except (socket.timeout, ConnectionRefusedError, OSError):
                    continue
                return connection

    def initiate_atomic_swap(self, sender_address: str, recipient_address: str, value: float, txin: tuple):
        raise NotImplementedError

    @staticmethod
    def dict_to_namedtuple(dictionary):
        return namedtuple('GenericDict', dictionary.keys())(**dictionary)
