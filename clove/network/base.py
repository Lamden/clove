class BaseNetwork(object):

    name = None
    symbols = ()

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
