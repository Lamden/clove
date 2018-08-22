from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch

import pytest
from pytest import mark, raises

from .constants import (
    eth_initial_transaction,
    eth_redeem_tranaction,
    eth_unsupported_transaction,
    token_initial_transaction,
)

from clove.constants import ETH_REDEEM_GAS_LIMIT, ETH_REFUND_GAS_LIMIT
from clove.exceptions import ImpossibleDeserialization, UnsupportedTransactionType
from clove.network import BitcoinTestNet, EthereumClassic, EthereumTestnet
from clove.network.ethereum.token import EthToken
from clove.network.ethereum.transaction import EthereumAtomicSwapTransaction
from clove.network.ethereum_based import Token


def test_atomic_swap(infura_token, web3_request_mock):
    alice_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    bob_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    network = EthereumTestnet()
    eth_atomic_swap = network.atomic_swap(sender_address=alice_address, recipient_address=bob_address, value=3)
    assert isinstance(eth_atomic_swap, EthereumAtomicSwapTransaction)


@mark.parametrize('address,valid', [
    ('0x999F348959E611F1E9eab2927c21E88E48e6Ef45', True),
    ('123', False),
    ('999F348959E611F1E9eab2927c21E88E48e6Ef45', False),
])
def test_ethereum_addresses(address, valid, infura_token):
    network = EthereumTestnet()
    assert network.is_valid_address(address) is valid


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_eth_audit_contract(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    assert contract.show_details() == {
        'confirmations': 11177,
        'contract_address': '0xce07aB9477BC20790B88B398A2A9e0F626c7D263',
        'locktime': datetime(2018, 8, 18, 14, 28, 10),
        'recipient_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
        'refund_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
        'secret_hash': 'ed2e6fe492005de2dd82e84d38448467d632e81c',
        'transaction_address': '0xcf64ef4d0449cf7a78d2be1c1f7225dffb11dded98a58d569ebcc6e883ce9f2b',
        'value': Decimal('0.001'),
        'value_text': '0.001000000000000000 ETH'
    }


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_participate_transaction(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')

    alice_eth_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    bob_eth_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    participate_value = 0.5

    participate_transaction = contract.participate(
        'ETH-TESTNET', alice_eth_address, bob_eth_address, participate_value
    )

    assert participate_transaction.sender_address == alice_eth_address
    assert participate_transaction.recipient_address == bob_eth_address
    assert participate_transaction.value == participate_value
    assert participate_transaction.secret_hash.hex() == contract.secret_hash
    assert participate_transaction.secret is None
    assert isinstance(participate_transaction.network, EthereumTestnet)


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_participate_token_transaction(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')

    alice_eth_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    bob_eth_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    token_address = '0x53E546387A0d054e7FF127923254c0a679DA6DBf'
    participate_value = 0.5

    participate_transaction = contract.participate(
        'ETH-TESTNET', alice_eth_address, bob_eth_address, participate_value, token_address=token_address
    )

    assert participate_transaction.sender_address == alice_eth_address
    assert participate_transaction.recipient_address == bob_eth_address
    assert participate_transaction.value == participate_value
    assert participate_transaction.token_address == token_address
    assert participate_transaction.secret_hash.hex() == contract.secret_hash
    assert participate_transaction.secret is None
    assert isinstance(participate_transaction.network, EthereumTestnet)


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_participate_btc_transaction(
    transaction_mock,
    infura_token,
    web3_request_mock,
    alice_wallet,
    bob_wallet,
    bob_utxo
):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')

    participate_value = 0.5
    participate_transaction = contract.participate(
        'BTC-TESTNET', bob_wallet.address, alice_wallet.address, participate_value, bob_utxo
    )

    assert participate_transaction.sender_address == bob_wallet.address
    assert participate_transaction.recipient_address == alice_wallet.address
    assert participate_transaction.value == participate_value
    assert participate_transaction.secret_hash.hex() == contract.secret_hash
    assert participate_transaction.secret is None
    assert isinstance(participate_transaction.network, BitcoinTestNet)


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(token_initial_transaction, ))
def test_token_audit_contract(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x316d3aaa252adb025c3486cf83949245f3f10edc169e1eb0772ed074fddb8be6')
    assert contract.show_details() == {
        'confirmations': 487,
        'contract_address': '0xce07aB9477BC20790B88B398A2A9e0F626c7D263',
        'locktime': datetime(2018, 8, 19, 12, 29, 44),
        'recipient_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
        'refund_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
        'secret_hash': '34378f0187488d019d3e0151f2fe3d3672ca310e',
        'transaction_address': '0x224818e4390e6d4e24b18e19a268825c0bbc649ab3e93dcb446328973dc7914b',
        'value': Decimal('1000'),
        'value_text': '1000.000000000000000000 BBT',
        'token_address': '0x53E546387A0d054e7FF127923254c0a679DA6DBf',
    }


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_unsupported_transaction, ))
def test_eth_audit_contract_unsupported_transaction(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    with pytest.raises(UnsupportedTransactionType) as error:
        network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    assert error.value.message.startswith('Unrecognized method id')


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_redeem_tranaction, ))
def test_eth_extract_secret(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    secret = network.extract_secret_from_redeem_transaction(
        '0x89b0d28e93ce55da4adab989cd48a524402eb154b23e1777f82e715589aba317'
    )
    assert secret == 'bc2424e1dcdd2e425c555bcea35a54fd27cf540e60f18366e153e3fb7cf4490c'


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_eth_refund(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    contract.locktime = datetime.utcnow() - timedelta(days=1)
    refund_transaction = contract.refund()
    details = refund_transaction.show_details()
    assert details['data'] == '0xf66c75e5ed2e6fe492005de2dd82e84d38448467d632e81c00000000000000000000' \
                              '0000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a9092'
    assert details['gas_limit'] == ETH_REFUND_GAS_LIMIT
    assert details['to'] == '0xce07ab9477bc20790b88b398a2a9e0f626c7d263'
    assert details['value'] == Decimal('0.001')
    assert details['value_text'] == '0.001000000000000000 ETH'
    assert details['recipient_address'] == '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    assert details['transaction'] == refund_transaction.raw_transaction


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_eth_refund_locktime(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    contract.locktime = datetime.utcnow() + timedelta(days=1)
    with pytest.raises(RuntimeError) as error:
        contract.refund()
    locktime_string = contract.locktime.strftime('%Y-%m-%d %H:%M:%S')
    assert str(error.value) == f"This contract is still valid! It can't be refunded until {locktime_string} UTC."


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_eth_redeem(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    redeem_transaction = contract.redeem('c037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac')
    details = redeem_transaction.show_details()
    assert details['data'] == '0xeda1122cc037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac'
    assert details['gas_limit'] == ETH_REDEEM_GAS_LIMIT
    assert details['to'] == '0xce07ab9477bc20790b88b398a2a9e0f626c7d263'
    assert details['value'] == Decimal('0.001')
    assert details['value_text'] == '0.001000000000000000 ETH'
    assert details['recipient_address'] == '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    assert details['transaction'] == redeem_transaction.raw_transaction


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(token_initial_transaction, ))
def test_eth_token_redeem(transaction_mock, infura_token, web3_request_mock):
    network = EthereumTestnet()
    contract = network.audit_contract('0x316d3aaa252adb025c3486cf83949245f3f10edc169e1eb0772ed074fddb8be6')
    redeem_transaction = contract.redeem('c037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac')
    details = redeem_transaction.show_details()
    assert details['data'] == '0xeda1122cc037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac'
    assert details['gas_limit'] == ETH_REDEEM_GAS_LIMIT
    assert details['to'] == '0xce07ab9477bc20790b88b398a2a9e0f626c7d263'
    assert details['value'] == Decimal('1000')
    assert details['value_text'] == '1000.000000000000000000 BBT'
    assert details['recipient_address'] == '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    assert details['transaction'] == redeem_transaction.raw_transaction


def test_approve_token(infura_token, web3_request_mock):
    network = EthereumTestnet()
    approve_tx = network.approve_token(
        '0x999f348959e611f1e9eab2927c21e88e48e6ef45',
        '0.001',
        '0x53E546387A0d054e7FF127923254c0a679DA6DBf'
    )
    details = approve_tx.show_details()
    assert details['value'] == Decimal('0.001')
    assert details['value_text'] == '0.001000000000000000 BBT'
    assert details['token_address'] == approve_tx.token.token_address
    assert details['sender_address'] == network.unify_address('0x999f348959e611f1e9eab2927c21e88e48e6ef45')
    assert details['transaction'] == approve_tx.raw_transaction


def test_token_atomic_swap(infura_token, web3_request_mock):
    alice_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    bob_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    network = EthereumTestnet()
    swap_tx = network.atomic_swap(
        sender_address=alice_address,
        recipient_address=bob_address,
        value='0.0003',
        token_address='0x53E546387A0d054e7FF127923254c0a679DA6DBf',
    )
    details = swap_tx.show_details()
    assert details['sender_address'] == alice_address
    assert details['recipient_address'] == bob_address
    assert details['contract_address'] == network.contract_address
    assert details['value'] == Decimal('0.0003')
    assert details['value_text'] == '0.000300000000000000 BBT'
    assert details['token_address'] == swap_tx.token.token_address
    assert details['transaction'] == swap_tx.raw_transaction


def test_get_token_from_token_contract(infura_token):

    network = EthereumTestnet()
    token = network.get_token_from_token_contract('0x53E546387A0d054e7FF127923254c0a679DA6DBf')
    assert token == Token(
        name='BlockbustersTest',
        symbol='BBT',
        address='0x53E546387A0d054e7FF127923254c0a679DA6DBf',
        decimals=18,
    )


def test_get_token_by_address(infura_token):

    network = EthereumTestnet()
    token = network.get_token_by_address('0x53E546387A0d054e7FF127923254c0a679DA6DBf')
    assert token.name == 'BlockbustersTest'
    assert token.symbol == 'BBT'
    assert token.token_address == '0x53E546387A0d054e7FF127923254c0a679DA6DBf'


@mark.parametrize('base_unit_value,float_value', [
    (10 ** (18-n), float(f'1e-{n}')) for n in range(18, 1, -1)
])
def test_token_value_base_units_conversion(base_unit_value, float_value):
    token = EthToken()
    assert token.value_to_base_units(float_value) == base_unit_value
    assert token.value_from_base_units(base_unit_value) == Decimal(str(float_value))


@mark.parametrize('value,token_decimals', [
    (Decimal(f'1e-{n}'), n-1) for n in range(1, 20, 2)
] + [
    (Decimal('9.9999'), 3),
    (Decimal('999.9999'), 3),
    (Decimal('999999.9999'), 3),
    (Decimal('999999999.9999'), 3),
])
def test_token_precision_validation(value, token_decimals):
    token = EthToken.from_namedtuple(Token('Test_token', 'TST', '0x123', token_decimals))
    with pytest.raises(ValueError) as error:
        token.validate_precision(value)
    assert str(error.value) == f'Test_token token supports at most {token_decimals} decimal places.'


@mark.parametrize('raw_transaction', ['', 'non_hex_characters', '12345'])
def test_deserialize_raw_transaction_invalid_transaction(raw_transaction):
    with raises(ImpossibleDeserialization):
        EthereumTestnet.deserialize_raw_transaction(raw_transaction)


def test_deserialize_raw_transaction():
    transaction = EthereumTestnet.deserialize_raw_transaction(eth_initial_transaction['raw'].hex())

    assert EthereumTestnet.unify_address(transaction.to.hex()) == eth_initial_transaction['to']
    assert EthereumTestnet.unify_address(transaction.sender.hex()) == eth_initial_transaction['from']
    assert transaction.hash == eth_initial_transaction['hash']
    assert transaction.nonce == eth_initial_transaction['nonce']
    assert transaction.gasprice == eth_initial_transaction['gasPrice']
    assert transaction.startgas == eth_initial_transaction['gas']
    assert transaction.value == eth_initial_transaction['value']
    assert transaction.data.hex() == eth_initial_transaction['input'][2:]
    assert transaction.s == int.from_bytes(eth_initial_transaction['s'], byteorder='big')
    assert transaction.r == int.from_bytes(eth_initial_transaction['r'], byteorder='big')
    assert transaction.v == eth_initial_transaction['v']


@mark.parametrize('private_key', ['', 'non_hex_characters', '12345'])
def test_sign_raw_transaction_invalid_key(private_key):
    unsigned_transaction = '0xf86880843b9aca0082b2089453e546387a0d054e7ff127923254c' \
                           '0a679da6dbf80b844095ea7b30000000000000000000000007657ca' \
                           '877fac31d20528b473162e39b6e152fd2e000000000000000000000' \
                           '00000000000000000000000003635c9adc5dea00000808080'

    with raises(ValueError, match='Invalid private key.'):
        EthereumTestnet.sign_raw_transaction(unsigned_transaction, private_key)


def test_sign_raw_transaction():
    unsigned_transaction = '0xf86880843b9aca0082b2089453e546387a0d054e7ff127923254c' \
                           '0a679da6dbf80b844095ea7b30000000000000000000000007657ca' \
                           '877fac31d20528b473162e39b6e152fd2e000000000000000000000' \
                           '00000000000000000000000003635c9adc5dea00000808080'

    private_key = '34fff148b3d00c1e8b3a016c7859e1616dc0edcfc3ea1ef7c96a7c4487fbeb26'
    address = '0x76cF367Efb63E037E3dfd0352DAc15e501f72DeA'

    raw_signed_transaction = EthereumTestnet.sign_raw_transaction(unsigned_transaction, private_key)
    signed_transaction = EthereumTestnet.deserialize_raw_transaction(raw_signed_transaction)

    assert EthereumTestnet.unify_address(signed_transaction.sender.hex()) == address


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_find_secret(transaction_mock, web3_request_mock):
    network = EthereumClassic()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    assert contract.find_secret() == 'bc2424e1dcdd2e425c555bcea35a54fd27cf540e60f18366e153e3fb7cf4490c'


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_find_redeem_transaction_in_event(transaction_mock, web3_request_mock):
    network = EthereumClassic()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    assert contract.find_redeem_transaction() == '0x65320e57b9d18ec08388896b029ad1495beb7a57c547440253a1dde01b4485f1'
