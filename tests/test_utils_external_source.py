from unittest.mock import patch

from pytest import mark

from clove.constants import CRYPTOID_SUPPORTED_NETWORKS
from clove.utils.external_source import (
    extract_scriptsig_from_redeem_transaction,
    get_balance_blockcypher,
    get_balance_cryptoid,
)


@mark.parametrize('network', ('btc', 'doge', 'dash'))
@patch('clove.utils.external_source.clove_req_json')
def test_extract_scriptsig_from_redeem_transaction_blockcypher(req_mock, network):
    # minimal version of required json object
    req_mock.return_value = {
        "txs": [
            {
                "hash": "011",
                "inputs": [
                    {
                        "script": "test-sigscript",
                        "script_type": "pay-to-script-hash"
                    }
                ]
            },
            {
                "hash": "010"
            }
        ]
    }
    assert 'test-sigscript' == extract_scriptsig_from_redeem_transaction(network, 'some_address')

    if network == 'btc':
        assert 'test-sigscript' == extract_scriptsig_from_redeem_transaction(network, 'some_address', testnet=True)


@mark.parametrize('network', ('btc', 'doge', 'dash'))
@patch('clove.utils.external_source.clove_req_json')
def test_extract_scriptsig_from_redeem_transaction_blockcypher_no_redeem(req_mock, network):
    # minimal version of required json response
    req_mock.return_value = {
        "txs": [
            {
                "hash": "010"
            }
        ]
    }
    assert extract_scriptsig_from_redeem_transaction(network, 'some_address') is None

    if network == 'btc':
        assert extract_scriptsig_from_redeem_transaction(network, 'some_address', testnet=True) is None


@mark.parametrize('network', CRYPTOID_SUPPORTED_NETWORKS[:2])
@patch('clove.utils.external_source.clove_req_json')
def test_extract_scriptsig_from_redeem_transaction_cryptoid(req_mock, network):
    # minimal versions of required json responses
    response1 = {
        "txs": [
            {
                "hash": "hash1"
            },
            {
                "hash": "hash2"
            }
        ]
    }
    response2 = {
        "vin": [
            {
                "scriptSig": {
                    "hex": "test-sigscript"
                }
            },
        ]
    }
    req_mock.side_effect = [response1, response2]
    assert "test-sigscript" == extract_scriptsig_from_redeem_transaction(
        network,
        'some_address',
        cryptoid_api_key='xxx'
    )


@mark.parametrize('network', CRYPTOID_SUPPORTED_NETWORKS[:2])
@patch('clove.utils.external_source.clove_req_json')
def test_extract_scriptsig_from_redeem_transaction_cryptoid_no_redeem(req_mock, network):
    # minimal version of required json response
    req_mock.return_value = {
        "txs": [
            {
                "hash": "hash1"
            }
        ]
    }
    assert extract_scriptsig_from_redeem_transaction(
        network,
        'some_address',
        cryptoid_api_key='xxx'
    ) is None


@patch('clove.utils.external_source.clove_req_json', return_value={'balance': 1000000})
def test_get_balance_blockcypher(clove_req_json_mock):
    balance = get_balance_blockcypher('BTC', '2Mv9q2BF9ua62vZcWQqtGdaaAki37SHVoXm', True)
    assert balance == 0.01
    clove_req_json_mock.assert_called_with(
        'https://api.blockcypher.com/v1/btc/test3/addrs/2Mv9q2BF9ua62vZcWQqtGdaaAki37SHVoXm/full?limit=2000'
    )


@patch('clove.utils.external_source.clove_req_json', return_value=0.001)
def test_get_balance_cryptoid(clove_req_json_mock):
    balance = get_balance_cryptoid('LTC', 'MAyEizEWZEQdd4Ghp7Es3ssN77d7yLbqZQ', False, cryptoid_api_key='123')
    assert balance == 0.001
    clove_req_json_mock.assert_called_with(
        'https://chainz.cryptoid.info/ltc/api.dws?q=getbalance&a=MAyEizEWZEQdd4Ghp7Es3ssN77d7yLbqZQ&key=123'
    )
