from bitcoin.core import COIN
from pytest import mark

from clove.utils.bitcoin import btc_to_satoshi, satoshi_to_btc


@mark.parametrize('btc_value', [0, 1, 10**(-9)])
def test_btc_to_satoshi(btc_value):
    satoshi_value = btc_to_satoshi(btc_value)

    assert isinstance(satoshi_value, int)
    assert satoshi_value == round(btc_value * COIN)


@mark.parametrize('satoshi_value', [0, 1, 10**8])
def test_satoshi_to_btc(satoshi_value):
    btc_value = satoshi_to_btc(satoshi_value)

    assert isinstance(btc_value, float)
    assert btc_value == satoshi_value / COIN
