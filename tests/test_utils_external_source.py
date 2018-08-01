from unittest.mock import patch

from pytest import mark

from .constants import eth_contract, eth_token_contract, etherscan_internal_transactions, etherscan_token_transfers

from clove.constants import CRYPTOID_SUPPORTED_NETWORKS
from clove.network import EthereumTestnet
from clove.utils.external_source import (
    extract_scriptsig_from_redeem_transaction,
    find_redeem_transaction,
    get_balance_blockcypher,
    get_balance_cryptoid,
    get_latest_block_number,
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


@patch('clove.utils.external_source.clove_req_json', return_value=etherscan_internal_transactions)
def test_find_redeem_transaction(_, etherscan_token):
    tx = find_redeem_transaction(
        '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'.lower(),
        '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8'.lower(),
        500000000000000000,
        'api-kovan',
    )
    assert tx == '0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1'


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', return_value=eth_contract)
@patch('clove.network.bitcoin.contract.get_balance', return_value=0.01)
@patch('clove.utils.external_source.clove_req_json', return_value=etherscan_internal_transactions)
def test_find_redeem_transaction_from_contract(_, balance_mock, contract_mock, infura_token, etherscan_token):
    eth_testnet = EthereumTestnet()
    contract = eth_testnet.audit_contract('0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f')
    tx = contract.find_redeem_transaction()
    assert tx == '0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1'


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', return_value=eth_token_contract)
@patch('clove.network.bitcoin.contract.get_balance', return_value=0.01)
@patch('clove.utils.external_source.clove_req_json', return_value=etherscan_token_transfers)
def test_find_redeem_token_transaction_from_contract(_, balance_mock, contract_mock, infura_token, etherscan_token):
    eth_testnet = EthereumTestnet()
    contract = eth_testnet.audit_contract('0x270cc74bf60fd0d37806b000a11da972ce240fa7478e38d8b44b6793ddd3284d')
    tx = contract.find_redeem_transaction()
    assert tx == '0x329f4bffbb5385bec8816740c5e423a91b89583e6952b16b644a48157f556269'


@patch('clove.utils.external_source.clove_req_json', return_value={
    'height': 1234,
})
def test_get_latest_block_blockcypher(clove_req_json_mock):
    latest_block_number = get_latest_block_number('BTC', testnet=True)
    assert latest_block_number == 1234
    clove_req_json_mock.assert_called_with(
        'https://api.blockcypher.com/v1/btc/test3/'
    )


@patch('clove.utils.external_source.clove_req_json', return_value=1234)
def test_get_latest_block_cryptoid(clove_req_json_mock):
    latest_block_number = get_latest_block_number('LTC')
    assert latest_block_number == 1234
    clove_req_json_mock.assert_called_with(
        'https://chainz.cryptoid.info/ltc/api.dws?q=getblockcount'
    )


@patch('clove.utils.external_source.clove_req_json', return_value=1234)
def test_get_latest_block_ravencoin(clove_req_json_mock):
    latest_block_number = get_latest_block_number('RVN')
    assert latest_block_number == 1234
    clove_req_json_mock.assert_called_with(
        'http://raven-blockchain.info/api/getblockcount'
    )
