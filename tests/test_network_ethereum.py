from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from .conftest import eth_initial_transaction, eth_redeem_tranaction

from clove.constants import ETH_REFUND_GAS_LIMIT
from clove.network import EthereumTestnet
from clove.network.ethereum.transaction import EthereumAtomicSwapTransaction


def test_atomic_swap(infura_token):
    alice_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    bob_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    network = EthereumTestnet()
    eth_atomic_swap = network.atomic_swap(sender_address=alice_address, recipient_address=bob_address, value=3)
    assert isinstance(eth_atomic_swap, EthereumAtomicSwapTransaction)


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_eth_audit_contract(transaction_mock, infura_token):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    assert contract.show_details() == {
        'contract_address': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
        'locktime': datetime(2018, 3, 30, 11, 56, 26),
        'recipient_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
        'refund_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
        'secret_hash': '10ff972f3d8181f603aa7f6b4bc172de730fec2b',
        'transaction_address': '0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41',
        'value': 12,
        'value_text': '0.000000000000000012 ETH'
    }


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_redeem_tranaction, ))
def test_eth_extract_secret(transaction_mock, infura_token):
    network = EthereumTestnet()
    secret = network.extract_secret_from_redeem_transaction(
        '0x89b0d28e93ce55da4adab989cd48a524402eb154b23e1777f82e715589aba317'
    )
    assert secret == '1e5a567ab04cc900c3da01d1b61c1a3755d648410963c3d0767ed2e0138e03a1'


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_eth_refund(transaction_mock, infura_token):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    contract.locktime = datetime.utcnow() - timedelta(days=1)
    refund_transaction = contract.refund()
    details = refund_transaction.show_details()
    assert details['data'] == '0x5a8f9b8110ff972f3d8181f603aa7f6b4bc172de730fec2b000000000000000000000000'
    assert details['hash'] == '0x546310fa12a51856138acd182e7cad4895b79aa5d6dca58b3554b7625330b434'
    assert details['startgas'] == ETH_REFUND_GAS_LIMIT
    assert details['to'] == '0x9f7e5402ed0858ea0c5914d44b900a42c89547b8'
    assert details['value'] == 0


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', side_effect=(eth_initial_transaction, ))
def test_eth_refund_locktime(transaction_mock, infura_token):
    network = EthereumTestnet()
    contract = network.audit_contract('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41')
    contract.locktime = datetime.utcnow() + timedelta(days=1)
    with pytest.raises(RuntimeError) as error:
        contract.refund()
    locktime_string = contract.locktime.strftime('%Y-%m-%d %H:%M:%S')
    assert str(error.value) == f"This contract is still valid! It can't be refunded until {locktime_string} UTC."
