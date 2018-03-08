from bitcoin.core import COIN
from pytest import mark

from clove.utils.bitcoin import from_base_units, to_base_units


@mark.parametrize('btc_value', [0, 1, 10**(-9)])
def test_to_base_units(btc_value):
    satoshi_value = to_base_units(btc_value)

    assert isinstance(satoshi_value, int)
    assert satoshi_value == round(btc_value * COIN)


@mark.parametrize('satoshi_value', [0, 1, 10**8])
def test_from_base_units(satoshi_value):
    btc_value = from_base_units(satoshi_value)

    assert isinstance(btc_value, float)
    assert btc_value == satoshi_value / COIN
