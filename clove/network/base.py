class BaseNetwork(object):
    '''Class for shared properties and methods for Bitcoin and Ethereum network.'''

    name = None
    '''Network name.'''
    symbols = ()
    '''Tuple with network symbols (some networks may have multiple symbols, eg. Bitcoin).'''
    networks = {}
    '''Placeholder for symbol-network mapping.'''
    bitcoin_based = None
    '''Flag for Bitcoin-based networks.'''
    ethereum_based = None
    '''Flag for Ethereum-based networks.'''
    testnet = False
    '''Flag for test networks.'''

    @property
    def default_symbol(self) -> str:
        '''Returns default (first) symbol for networks with multiple symbols.

        Returns:
            str: network symbol

        Example:
            >>> from clove.network import Bitcoin
            >>> bitcoin_network = Bitcoin()
            >>> bitcoin_network.default_symbol
            'BTC'

        Note:
            This property can return `None` if `symbols` are not declared in the network definition.
        '''
        if self.symbols:
            return self.symbols[0]

    @classmethod
    def is_test_network(cls) -> bool:
        '''Returning True if the network is a testnet.'''
        return cls.testnet

    @classmethod
    def get_network_by_symbol(cls, symbol: str):
        '''
        Returns network instance by its symbol.

        Args:
            str: network symbol

        Returns:
            Network object

        Raises:
            RuntimeError: if there is no network with given symbol.

        Example:
            >>> from clove.network.base import BaseNetwork
            >>> BaseNetwork.get_network_by_symbol('BTC')
            <clove.network.bitcoin.Bitcoin at 0x7f5a84b233c8>

        '''
        if not cls.networks:
            cls.set_symbol_mapping()

        symbol = symbol.upper()

        if symbol not in cls.networks:
            raise RuntimeError(f'{symbol} network is not supported.')

        return cls.networks[symbol]()

    @classmethod
    def set_symbol_mapping(cls):
        '''Creates symbol-instance mapping.'''
        from clove.network import __all__ as networks
        for network in networks:
            for symbol in network.symbols:
                if network.is_test_network():
                    cls.networks[f'{symbol.upper()}-TESTNET'] = network
                else:
                    cls.networks[f'{symbol.upper()}'] = network
