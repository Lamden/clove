from bitcoin.core import COIN


def satoshi_to_btc(value):
    return value / COIN


def btc_to_satoshi(value):
    return round(value * COIN)
