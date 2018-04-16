class BaseNetwork(object):

    name = None
    symbols = ()
    networks = {}
    test_networks = {}
    bitcoin_based = None
    ethereum_based = None
    testnet = False

    @property
    def default_symbol(self):
        if self.symbols:
            return self.symbols[0]

    @classmethod
    def is_test_network(cls):
        return cls.testnet

    @classmethod
    def get_network_by_symbol(cls, symbol):

        if not cls.networks:
            cls.set_symbol_mapping()

        symbol = symbol.upper()

        if symbol not in cls.networks:
            raise RuntimeError(f'{symbol} network is not supported.')

        return cls.networks[symbol]()

    @classmethod
    def set_symbol_mapping(cls):
        from clove.network import __all__ as networks
        for network in networks:
            for symbol in network.symbols:
                if network.is_test_network():
                    cls.networks[f'{symbol.upper()}-TESTNET'] = network
                else:
                    cls.networks[f'{symbol.upper()}'] = network
