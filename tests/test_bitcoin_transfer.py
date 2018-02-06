from datetime import datetime
from unittest.mock import patch

from bitcoin.core import COIN

from clove.network.bitcoin import BitcoinTestNet, BitcoinTransaction


def test_swap_contract(alice_wallet, bob_wallet):
    transaction = BitcoinTransaction(
        BitcoinTestNet(),
        alice_wallet.get_address(),
        bob_wallet.get_address(),
        0.5,
        outpoints={}
    )
    transaction.set_locktime(number_of_hours=48)
    transaction.generate_hash()
    transaction.build_atomic_swap_contract()
    assert transaction.contract.is_valid()


def test_transaction_signing(alice_wallet, unsigned_transaction):
    transaction = unsigned_transaction
    first_script_signature = transaction.tx.vin[0].scriptSig
    transaction.sign(alice_wallet)
    second_first_script_signature = transaction.tx.vin[0].scriptSig
    assert first_script_signature != second_first_script_signature


def test_show_details(signed_transaction):
    details = signed_transaction.show_details()

    assert type(details) is dict

    str_fields = (
        'contract',
        'contract_transaction',
        'contract_transaction_hash',
        'recipient_address',
        'refund_address',
        'secret',
        'secret_hash',
        'size_text',
        'value_text',
        'fee_text',
        'fee_per_kb_text',
    )

    date_fields = (
        'locktime',
    )

    int_fields = (
        'size',
    )

    float_fields = (
        'value',
        'fee',
        'fee_per_kb',
    )

    for field in str_fields:
        assert type(details[field]) is str, 'not a string'
        assert len(details[field]), 'empty string'

    for field in date_fields:
        assert type(details[field]) is datetime, 'not a datetime'

    for field in float_fields:
        assert type(details[field]) is float, 'not a float'

    assert details['value'] == signed_transaction.value
    assert details['value_text'] == '0.70000000 BTC'

    assert details['fee_per_kb_text'].endswith('/ 1 kB')
    assert details['size_text'].endswith('bytes')

    assert sorted(details.keys()) == sorted(str_fields + date_fields + int_fields + float_fields)


@patch('clove.network.base.BaseNetwork.get_current_fee_per_kb', return_value=0.002)
def test_transaction_fee(fee_per_kb_mock, unsigned_transaction):

    assert type(unsigned_transaction.size) == int

    unsigned_transaction.add_fee()
    assert type(unsigned_transaction.fee) == float
    assert unsigned_transaction.fee < 1, 'Transaction fee should be in main units'

    change_without_fee = unsigned_transaction.tx.vout[1].nValue
    unsigned_transaction.add_fee()
    change_with_fee = unsigned_transaction.tx.vout[1].nValue

    assert change_without_fee - unsigned_transaction.fee * COIN == change_with_fee
    assert unsigned_transaction.tx.serialize()
