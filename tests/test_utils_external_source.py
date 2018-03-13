from unittest.mock import patch

from pytest import mark

from clove.constants import CRYPTOID_SUPPORTED_NETWORKS
from clove.utils.external_source import extract_scriptsig_from_redeem_transaction


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
