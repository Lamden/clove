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
