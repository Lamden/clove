from datetime import datetime, timedelta
from unittest.mock import patch

from bitcoin.core import CTransaction, b2x, script
from freezegun import freeze_time
from pytest import raises

from clove.constants import SIGNATURE_SIZE
from clove.network import BitcoinTestNet, Litecoin
from clove.network.bitcoin.transaction import BitcoinAtomicSwapTransaction, BitcoinTransaction
from clove.utils.bitcoin import to_base_units


def test_swap_contract(alice_wallet, bob_wallet):
    transaction = BitcoinAtomicSwapTransaction(
        BitcoinTestNet(),
        alice_wallet.address,
        bob_wallet.address,
        0.5,
        solvable_utxo=[]
    )
    transaction.set_locktime(number_of_hours=48)
    transaction.generate_hash()
    transaction.build_atomic_swap_contract()
    assert transaction.contract.is_valid()


def test_transaction_signing(unsigned_transaction):
    transaction = unsigned_transaction
    first_script_signature = transaction.tx.vin[0].scriptSig
    transaction.sign()
    second_first_script_signature = transaction.tx.vin[0].scriptSig
    assert first_script_signature != second_first_script_signature


def test_transaction_signing_with_default_wallet(alice_wallet, unsigned_transaction):
    transaction = unsigned_transaction
    unsigned_transaction.solvable_utxo[0].wallet = None
    with raises(
        RuntimeError,
        match="Cannot sign transaction without a wallet."
    ):
        transaction.sign()

    first_script_signature = transaction.tx.vin[0].scriptSig
    transaction.sign(alice_wallet)
    second_first_script_signature = transaction.tx.vin[0].scriptSig
    assert first_script_signature != second_first_script_signature


def test_show_details(signed_transaction):
    details = signed_transaction.show_details()

    assert type(details) is dict

    str_fields = (
        'contract',
        'contract_address',
        'contract_transaction',
        'transaction_address',
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


def test_transaction_fee(unsigned_transaction):

    assert type(unsigned_transaction.size) == int

    unsigned_transaction.fee_per_kb = 0.002
    unsigned_transaction.add_fee()
    assert type(unsigned_transaction.fee) == float
    assert unsigned_transaction.fee < 1, 'Transaction fee should be in main units'

    change_without_fee = unsigned_transaction.tx.vout[1].nValue
    unsigned_transaction.add_fee()
    change_with_fee = unsigned_transaction.tx.vout[1].nValue

    assert change_without_fee - to_base_units(unsigned_transaction.fee) == change_with_fee
    assert unsigned_transaction.tx.serialize()


def test_calculate_fee_with_signature_size(unsigned_transaction):

    fee_per_kb = 0.002
    unsigned_transaction.fee_per_kb = fee_per_kb
    unsigned_transaction.calculate_fee(add_sig_size=True)
    size_after_sign = unsigned_transaction.size + (SIGNATURE_SIZE * len(unsigned_transaction.tx_in_list))
    assert unsigned_transaction.fee == round(size_after_sign/1000 * fee_per_kb, 8)


def test_transaction_with_invalid_recipient_address():
    with raises(ValueError, match='Given recipient address is invalid.'):
        BitcoinTransaction(BitcoinTestNet(), 'invalid_address', 0.01, [])


def test_swap_transaction_with_invalid_recipient_address(bob_wallet):
    with raises(ValueError, match='Given recipient address is invalid.'):
        BitcoinAtomicSwapTransaction(BitcoinTestNet(), bob_wallet.address, 'invalid_address', 0.01, [])


def test_swap_transaction_with_invalid_sender_address(bob_wallet):
    with raises(ValueError, match='Given sender address is invalid.'):
        BitcoinAtomicSwapTransaction(BitcoinTestNet(), 'invalid_address', bob_wallet.address, 0.01, [])


def test_swap_transaction_with_invalid_recipient_and_sender_addresses():
    with raises(ValueError, match='Given recipient and sender addresses are invalid.'):
        BitcoinAtomicSwapTransaction(BitcoinTestNet(), 'invalid_address', 'address_123', 0.01, [])


def test_audit_contract(signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    contract_details = contract.show_details()

    assert contract.locktime == signed_transaction.locktime.replace(microsecond=0)

    contract_details.pop('locktime')

    for field in contract_details.keys():
        assert contract_details[field] == transaction_details[field]


def test_audit_contract_empty_transaction():
    btc_network = BitcoinTestNet()
    tx = b2x(CTransaction().serialize())

    with raises(
        ValueError, match='Given transaction has no outputs.'
    ):
        btc_network.audit_contract('', tx)


def test_audit_contract_invalid_transaction(signed_transaction):
    btc_network = BitcoinTestNet()
    signed_transaction.tx.vout.pop(0)
    transaction_details = signed_transaction.show_details()

    with raises(
        ValueError, match='Given transaction is not a valid contract.'
    ):
        btc_network.audit_contract(transaction_details['contract'], transaction_details['contract_transaction'])


def test_audit_contract_non_matching_contract(signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = script.CScript([script.OP_TRUE]).hex()

    with raises(
        ValueError, match='Given transaction is not a valid contract.'
    ):
        btc_network.audit_contract(contract, transaction_details['contract_transaction'])


def test_audit_contract_by_address_blockcypher():
    ltc_network = Litecoin()
    contract = ltc_network.audit_contract(
        contract=(
            '63a6140d33bfb2b425ca1d91a9a90af9472d6b7a6760d88876a914621f617c765c3caa5ce1bb67f6a'
            '3e51382b8da296704ab0ece5ab17576a91485c0522f6e23beb11cc3d066cd20ed732648a4e66888ac'
        ),
        transaction_address='2d08cb8a4c06c5df7d21334a0dff5aaebf55d1b3adb8545d707f2b45888f932b'
    )
    assert contract.show_details() == {
        'contract_address': 'MAyEizEWZEQdd4Ghp7Es3ssN77d7yLbqZQ',
        'locktime': datetime(2018, 4, 11, 13, 33, 31),
        'recipient_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
        'refund_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
        'secret_hash': '0d33bfb2b425ca1d91a9a90af9472d6b7a6760d8',
        'transaction_address': '2d08cb8a4c06c5df7d21334a0dff5aaebf55d1b3adb8545d707f2b45888f932b',
        'value': 0.001,
        'value_text': '0.00100000 LTC',
     }


@patch('clove.utils.external_source.BLOCKCYPHER_SUPPORTED_NETWORKS', return_value=('xxx', ))
def test_audit_contract_by_address_cryptoid(_):
    ltc_network = Litecoin()
    contract = ltc_network.audit_contract(
        contract=(
            '63a6140d33bfb2b425ca1d91a9a90af9472d6b7a6760d88876a914621f617c765c3caa5ce1bb67f6a'
            '3e51382b8da296704ab0ece5ab17576a91485c0522f6e23beb11cc3d066cd20ed732648a4e66888ac'
        ),
        transaction_address='2d08cb8a4c06c5df7d21334a0dff5aaebf55d1b3adb8545d707f2b45888f932b'
    )
    assert contract.show_details() == {
        'contract_address': 'MAyEizEWZEQdd4Ghp7Es3ssN77d7yLbqZQ',
        'locktime': datetime(2018, 4, 11, 13, 33, 31),
        'recipient_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
        'refund_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
        'secret_hash': '0d33bfb2b425ca1d91a9a90af9472d6b7a6760d8',
        'transaction_address': '2d08cb8a4c06c5df7d21334a0dff5aaebf55d1b3adb8545d707f2b45888f932b',
        'value': 0.001,
        'value_text': '0.00100000 LTC',
     }


def test_redeem_transaction(bob_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    redeem_transaction = contract.redeem(bob_wallet, transaction_details['secret'])
    redeem_transaction.fee_per_kb = 0.002
    redeem_transaction.add_fee_and_sign()

    assert redeem_transaction.recipient_address == bob_wallet.address
    assert redeem_transaction.value == signed_transaction.value


def test_refund_transaction(alice_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )

    with freeze_time(transaction_details['locktime']):
        refund_transaction = contract.refund(alice_wallet)

    refund_transaction.fee_per_kb = 0.002
    refund_transaction.add_fee_and_sign()

    assert refund_transaction.recipient_address == alice_wallet.address
    assert refund_transaction.value == signed_transaction.value


def test_refund_not_expired_contract(alice_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )

    with freeze_time(transaction_details['locktime'] - timedelta(seconds=1)):
        locktime_string = transaction_details['locktime'].strftime('%Y-%m-%d %H:%M:%S')
        with raises(
            RuntimeError, match=f"This contract is still valid! It can't be refunded until {locktime_string}."
        ):
            contract.refund(alice_wallet)


def test_participate_transaction(alice_wallet, bob_wallet, bob_utxo, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    participate_value = 0.5
    participate_transaction = contract.participate(
        'BTC-TESTNET', bob_wallet.address, alice_wallet.address, participate_value, bob_utxo
    )
    participate_transaction.fee_per_kb = 0.002
    participate_transaction.add_fee_and_sign()

    assert participate_transaction.sender_address == bob_wallet.address
    assert participate_transaction.recipient_address == alice_wallet.address
    assert participate_transaction.value == participate_value
    assert participate_transaction.secret_hash == signed_transaction.secret_hash
    assert participate_transaction.secret is None
    assert isinstance(participate_transaction.network, BitcoinTestNet)

    participate_transaction_details = participate_transaction.show_details()

    contract = btc_network.audit_contract(
        participate_transaction_details['contract'],
        participate_transaction_details['contract_transaction']
    )
    redeem_participate_transaction = contract.redeem(alice_wallet, transaction_details['secret'])
    redeem_participate_transaction.fee_per_kb = 0.002
    redeem_participate_transaction.add_fee_and_sign()

    assert redeem_participate_transaction.recipient_address == alice_wallet.address
    assert redeem_participate_transaction.value == participate_value


def test_extract_secret(bob_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    redeem_transaction = contract.redeem(bob_wallet, transaction_details['secret'])
    redeem_transaction.fee_per_kb = 0.002
    redeem_transaction.add_fee_and_sign()

    redeem_details = redeem_transaction.show_details()

    secret = btc_network.extract_secret(redeem_details['transaction'])

    assert secret == transaction_details['secret']

    # extracting secret from scriptSig
    assert secret == btc_network.extract_secret(scriptsig=redeem_transaction.tx.vin[0].scriptSig.hex())
