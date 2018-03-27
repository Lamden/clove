from clove.network.base import BaseNetwork


def get_network_by_symbol(symbol: str):
    try:
        return BaseNetwork.get_network_by_symbol(symbol)
    except RuntimeError:
        return
