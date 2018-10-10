from functools import wraps

from bitcoin.core import COIN


def from_base_units(value: int) -> float:
    '''
    Converting value from base units.

    Args:
        value (int): value in base units

    Returns:
        float: value in main coins

    Example:
        >>> from clove.utils.bitcoin import from_base_units
        >>> from_base_units(10000)
        0.0001
    '''
    return value / COIN


def to_base_units(value: float) -> int:
    '''
    Converting value from base units.

    Args:
        value (int): value in base units

    Returns:
        float: value in main coins

    Example:
        >>> from clove.utils.bitcoin import to_base_units
        >>> to_base_units(0.000001)
        100
    '''
    return round(value * COIN)


def auto_switch_params(args_index: int=0):
    '''
    Decorator for changing network parameters before running some method.

    Args:
        args_index (int): if network object was passed as an argument we can provide an index number of this argument.

    Example:
        >>> @auto_switch_params()
        >>> def connect(self) -> str:
    '''
    def wrap(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if 'network' in kwargs:
                kwargs['network'].switch_params()
            else:
                args[args_index].switch_params()
            return f(*args, **kwargs)
        return wrapped
    return wrap
