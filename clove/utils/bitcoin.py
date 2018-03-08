from bitcoin.core import COIN


def from_base_units(value):
    return value / COIN


def to_base_units(value):
    return round(value * COIN)
