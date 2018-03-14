from bitcoin.core import COIN, CTransaction
from pytest import mark, raises

from clove.exceptions import ImpossibleDeserialization
from clove.utils.bitcoin import deserialize_raw_transaction, from_base_units, to_base_units


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


def test_deserialize_raw_transaction():
    valid_transaction = '0100000001350ff23c56027e3f7b8206d01a8fa2302d7ef82898e7ac795674a4e6450dd427000000008a47' \
                        '3044022033a4d693aedc99fea12d03acb07d3fbd2c26eb1da88df2820a2544058010a750022032195aaed8' \
                        'e773fa984bb3fe98ab138f6af36a500151f910a473f437bd63631501410402282aa6329ceada82ebcd53af' \
                        '7b1739cbc958e137ddde2b5da21183fa545b54cf75ce0c2296af902d53dd2a06fd783b7d8de00d74e612e8' \
                        '52bfee952d6744e70000000002a0e92f000000000017a914a2e40d94f0fa9d2bb8b6f424607f44a2e153da' \
                        '6f87c059693b000000001976a9143dfd3bba567574ba0508d01a96e89300af292b0688ac00000000'
    invalid_transaction = 'I am invalid transaction :)'

    assert type(deserialize_raw_transaction(valid_transaction)) == CTransaction

    with raises(ImpossibleDeserialization):
        deserialize_raw_transaction(invalid_transaction)
