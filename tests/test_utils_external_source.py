from unittest.mock import patch

from hexbytes.main import HexBytes
from pytest import mark
from web3.utils.datastructures import AttributeDict

from clove.constants import CRYPTOID_SUPPORTED_NETWORKS
from clove.network import EthereumTestnet
from clove.utils.external_source import (
    extract_scriptsig_from_redeem_transaction,
    find_redeem_transaction,
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


def test_find_redeem_transaction(etherscan_api_response, etherscan_token):
    tx = find_redeem_transaction(
        '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'.lower(),
        '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8'.lower(),
        500000000000000000,
        'api-kovan'
    )
    assert tx == '0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1'


@patch('clove.network.ethereum.base.EthereumBaseNetwork.get_transaction', return_value=AttributeDict({
    'blockHash': HexBytes('0x9c581f507f5541fba0d5e3d897e46dcdffab497d59987ebe0337f89581e4d8cd'),
    'blockNumber': 6792738,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'gas': 126221,
    'gasPrice': 20000000000,
    'hash': HexBytes('0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f'),
    'input': (
        '0xeb8ae1ed000000000000000000000000000000000000000000000000000000005acca1d68cebcb1af6fa5fddeb'
        '091f61f0af1c49a6de9922000000000000000000000000000000000000000000000000999f348959e611f1e9eab2'
        '927c21e88e48e6ef45'
    ),
    'nonce': 18,
    'publicKey': HexBytes(
        '0x579c6126677857d4d5a227ed47efbd9742e26f60449e8ea6a536c0dd9b2fb6fb14e0fddc7cb06fd78d2c6c3ef4'
        'd1b72e488096504817ed7ac252b2453cbfab56'
    ),
    'r': HexBytes('0x165e3e1c366078a77491348daf306b9b2e9e2a2d884efb0c750fa9d701009b75'),
    'raw': HexBytes(
        '0xf8d2128504a817c8008301ed0d949f7e5402ed0858ea0c5914d44b900a42c89547b88806f05b59d3b20000b864'
        'eb8ae1ed000000000000000000000000000000000000000000000000000000005acca1d68cebcb1af6fa5fddeb09'
        '1f61f0af1c49a6de9922000000000000000000000000000000000000000000000000999f348959e611f1e9eab292'
        '7c21e88e48e6ef451ca0165e3e1c366078a77491348daf306b9b2e9e2a2d884efb0c750fa9d701009b75a04c6672'
        '33a3f4570964c58a0e145f3ace761315c05a0b8360fefe2b67f8e00eba'
    ),
    's': HexBytes('0x4c667233a3f4570964c58a0e145f3ace761315c05a0b8360fefe2b67f8e00eba'),
    'standardV': 1,
    'to': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'transactionIndex': 1,
    'v': 28,
    'value': 500000000000000000,
}))
@patch('clove.network.bitcoin.contract.get_balance', return_value=0.01)
def test_find_redeem_transaction_from_contract(_, contract_mock, etherscan_api_response, infura_token, etherscan_token):
    eth_testnet = EthereumTestnet()
    contract = eth_testnet.audit_contract('0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f')
    tx = contract.find_redeem_transaction()
    assert tx == '0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1'
