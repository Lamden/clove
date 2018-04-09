from functools import wraps

from bitcoin.core import COIN, CTransaction, x

from clove.exceptions import ImpossibleDeserialization


def from_base_units(value):
    return value / COIN


def to_base_units(value):
    return round(value * COIN)


def deserialize_raw_transaction(raw_transaction: str) -> CTransaction:
    try:
        return CTransaction.deserialize(x(raw_transaction))
    except Exception:
        raise ImpossibleDeserialization()


def auto_switch_params(args_index: int = 0):
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
