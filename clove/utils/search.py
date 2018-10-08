from clove.network.base import BaseNetwork


def get_network_by_symbol(symbol: str):
    '''
    Returns network instance by its symbol.

    Args:
        symbol (str): network symbol

    Returns:
        Network object

    Raises:
        RuntimeError: if there is no network with given symbol.

    Example:
        >>> from clove.utils.search import get_network_by_symbol
        >>> get_network_by_symbol('BTC')
        <clove.network.bitcoin.Bitcoin at 0x7f5a84b233c8>
    '''
    try:
        return BaseNetwork.get_network_by_symbol(symbol)
    except RuntimeError:
        return
