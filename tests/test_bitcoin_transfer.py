from datetime import datetime

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


def test_initiate_atomic_swap(alice_wallet, bob_wallet, alice_outpoints):
    btc_network = BitcoinTestNet()
    transaction = btc_network.initiate_atomic_swap(
        alice_wallet.get_address(),
        bob_wallet.get_address(),
        0.00001,
        alice_outpoints
    )
    first_script_signature = transaction.tx.vin[0].scriptSig
    transaction.sign(alice_wallet)
    second_first_script_signature = transaction.tx.vin[0].scriptSig
    assert first_script_signature != second_first_script_signature


def test_show_details(alice_wallet, bob_wallet, alice_outpoints):
    btc_network = BitcoinTestNet()
    transaction_value = 0.00001
    transaction = btc_network.initiate_atomic_swap(
        alice_wallet.get_address(),
        bob_wallet.get_address(),
        transaction_value,
        alice_outpoints
    )
    details = transaction.show_details()

    assert type(details) is dict

    str_fields = (
        'contract',
        'contract_transaction',
        'contract_transaction_hash',
        'recipient_address',
        'refund_address',
        'secret',
        'secret_hash',
        'value_text',
    )

    date_fields = (
        'locktime',
    )

    float_fields = (
        'value',
    )

    for field in str_fields:
        assert type(details[field]) is str, 'not a string'
        assert len(details[field]), 'empty string'

    for field in date_fields:
        assert type(details[field]) is datetime, 'not a datetime'

    for field in float_fields:
        assert type(details[field]) is float, 'not a float'

    assert details['value'] == transaction_value
    assert details['value_text'] == '0.00001000 BTC'

    assert sorted(details.keys()) == sorted(str_fields + date_fields + float_fields)
