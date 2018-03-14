from clove.network import Bitcoin, BitcoinTestNet


def get_network_object(symbol: str, testnet: bool = False):
    try:
        if testnet:
            return BitcoinTestNet.get_network_class_by_symbol(symbol)()
        return Bitcoin.get_network_class_by_symbol(symbol)()
    except RuntimeError:
        return
