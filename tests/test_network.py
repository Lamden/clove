import ipaddress
from unittest.mock import patch

import bitcoin
from bitcoin.core import CTransaction
import pytest
from pytest import mark, raises
from validators import domain

from clove.constants import CRYPTOID_SUPPORTED_NETWORKS
from clove.exceptions import ImpossibleDeserialization
from clove.network import BITCOIN_BASED as networks
from clove.network import BitcoinTestNet, Monacoin
from clove.network.bitcoin.base import BitcoinBaseNetwork
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import auto_switch_params
from clove.utils.search import get_network_by_symbol


@mark.parametrize('network', networks)
def test_bitcoin_based_network_definitions(network):
    assert isinstance(network.name, str)
    assert isinstance(network.symbols, tuple)
    assert isinstance(network().default_symbol, str)
    assert getattr(network, 'seeds') or getattr(network, 'nodes'), f'[{network.__name__}] no seeds and nodes'
    if network.nodes:
        assert isinstance(network.nodes, tuple)
        assert not network.seeds, f'{network}: use nodes or seeds, not both.'
        for node in network.nodes:
            assert ipaddress.ip_address(node)
    else:
        assert isinstance(network.seeds, tuple)
        for seed in network.seeds:
            assert domain(seed)
    assert isinstance(network.port, int)
    assert isinstance(network.blacklist_nodes, dict)
    assert isinstance(network.message_start, bytes)
    assert isinstance(network.base58_prefixes, dict)
    assert isinstance(network.source_code_url, str)
    if network.blockexplorer_tx:
        assert isinstance(network.blockexplorer_tx, str)


def test_network_source_code_url_is_unique():
    mainnet_networks = [network for network in networks if not network.is_test_network()]
    source_code_urls_of_networks = set([network.source_code_url for network in mainnet_networks])
    assert len(mainnet_networks) == len(source_code_urls_of_networks)


@mark.parametrize('network', networks)
@patch('clove.network.bitcoin.base.get_current_fee', return_value=0.01)
def test_fee_per_kb_implementation(clove_api_mock, network):
    # networks supported by blockcypher or with own methods for getting fee
    if network.name in ('bitcoin', 'test-bitcoin', 'litecoin', 'dogecoin', 'dash', 'raven'):
        assert network.get_current_fee_per_kb() == 0.01
        return

    assert network.get_current_fee_per_kb() == 0.01


blockcypher_utxo_response = {
    "txrefs": [
        {
            "tx_hash": "e0832ca854e4577cab20413013d6251c4a426022112d9ff222067bb5d8b6b723",
            "block_height": 1371134,
            "tx_input_n": -1,
            "tx_output_n": 0,
            "value": 90000070,
            "ref_balance": 89713538526651,
            "spent": False,
            "confirmations": 9184,
            "confirmed": "2018-02-18T20:25:14Z",
            "double_spend": False,
            "script": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac"
        },
        {
            "tx_hash": "308b997d8583aa48a7b265246eb76e5d030495468bbb87989606aea769b03600",
            "block_height": 1370100,
            "tx_input_n": -1,
            "tx_output_n": 1,
            "value": 15500105,
            "ref_balance": 89713537626581,
            "spent": False,
            "confirmations": 10218,
            "confirmed": "2018-02-17T02:43:51Z",
            "double_spend": False,
            "script": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac"
        },
        {
            "tx_hash": "e7cc6e21b9f2d1d7bdc4fd40096ba74bc714f434c2dc5a5e414ad8c32235368a",
            "block_height": 1363362,
            "tx_input_n": -1,
            "tx_output_n": 1,
            "value": 10000000,
            "ref_balance": 89713537471476,
            "spent": False,
            "confirmations": 16956,
            "confirmed": "2018-02-05T17:29:10Z",
            "double_spend": False,
            "script": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac"
        },
    ]
}

cryptoid_utxo_response = {
    "unspent_outputs": [
        {
            "tx_hash": "e7cc6e21b9f2d1d7bdc4fd40096ba74bc714f434c2dc5a5e414ad8c32235368a",
            "tx_ouput_n": 1,
            "value": "10000000",
            "confirmations": 17040,
            "script": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac"
        }, {
            "tx_hash": "308b997d8583aa48a7b265246eb76e5d030495468bbb87989606aea769b03600",
            "tx_ouput_n": 1,
            "value": "15500105",
            "confirmations": 10302,
            "script": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac"
        }, {
            "tx_hash": "e0832ca854e4577cab20413013d6251c4a426022112d9ff222067bb5d8b6b723",
            "tx_ouput_n": 0,
            "value": "90000070",
            "confirmations": 9268,
            "script": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac"
        }
    ]
}

monacoin_utxo_response = [
  {
    "txid": "e0832ca854e4577cab20413013d6251c4a426022112d9ff222067bb5d8b6b723",
    "vout": 0,
    "scriptPubKey": {
      "asm": "OP_DUP OP_HASH160 098671104a3dd5b8eb1559929221d946073a34ba OP_EQUALVERIFY OP_CHECKSIG",
      "hex": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac",
      "type": "pubkeyhash",
      "address": "M8mXNKtwFoW765V8VEbhZ8TNCqywFr25in"
    },
    "value": 90000070
  },
  {
    "txid": "308b997d8583aa48a7b265246eb76e5d030495468bbb87989606aea769b03600",
    "vout": 1,
    "scriptPubKey": {
      "asm": "OP_DUP OP_HASH160 098671104a3dd5b8eb1559929221d946073a34ba OP_EQUALVERIFY OP_CHECKSIG",
      "hex": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac",
      "type": "pubkeyhash",
      "address": "M8mXNKtwFoW765V8VEbhZ8TNCqywFr25in"
    },
    "value": 15500105
  },
]

expected_utxo = [
    Utxo(
        tx_id='e0832ca854e4577cab20413013d6251c4a426022112d9ff222067bb5d8b6b723',
        vout=0,
        value=0.9000007,
        tx_script='76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac'
    ),
    Utxo(
        tx_id='308b997d8583aa48a7b265246eb76e5d030495468bbb87989606aea769b03600',
        vout=1,
        value=0.15500105,
        tx_script='76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac'
    )
]
expected_utxo_dicts = [utxo.__dict__ for utxo in expected_utxo]


@mark.parametrize('network', networks)
@patch('clove.utils.external_source.clove_req_json')
@patch.dict('os.environ', {'CRYPTOID_API_KEY': 'test_api_key'})
def test_getting_utxo(json_response, network):
    if network.name == 'monacoin':
        # there is a separate test for monacoin utxo
        return
    address = 'testaddress'
    amount = 1.0
    symbol = network.symbols[0].lower()
    # networks supported by blockcypher
    if network.name in ('test-bitcoin', 'dogecoin'):
        json_response.return_value = blockcypher_utxo_response

        assert [utxo.__dict__ for utxo in network.get_utxo(address, amount)] == expected_utxo_dicts

        assert json_response.call_args[0][0].startswith('https://api.blockcypher.com')
        return

    if network.is_test_network() or symbol not in CRYPTOID_SUPPORTED_NETWORKS:
        with pytest.raises(NotImplementedError):
            network.get_utxo(address, amount)
        return

    json_response.return_value = cryptoid_utxo_response

    assert [utxo.__dict__ for utxo in network.get_utxo(address, amount)] == expected_utxo_dicts
    assert json_response.call_args[0][0].startswith('https://chainz.cryptoid.info/')


@patch('clove.network.bitcoin_based.monacoin.clove_req_json', return_value=monacoin_utxo_response)
def test_getting_utxo_monacoin(json_response):
    network = Monacoin()
    address = 'testaddress'
    amount = 1.0
    assert [utxo.__dict__ for utxo in network.get_utxo(address, amount)] == expected_utxo_dicts
    assert json_response.call_args[0][0].startswith('https://mona.chainseeker.info/api/v1/utxos/')


def test_filter_blacklisted_nodes_method():
    network = BitcoinBaseNetwork()
    network.blacklist_nodes = {'107.150.122.31': 4, '107.170.239.46': 1, '108.144.213.98': 3, '13.113.121.156': 4}
    nodes = list(network.blacklist_nodes.keys()) + ['34.207.248.232']
    assert network.filter_blacklisted_nodes(nodes) == ['34.207.248.232', '107.170.239.46', '108.144.213.98']
    assert network.filter_blacklisted_nodes(nodes, max_tries_number=2) == ['34.207.248.232', '107.170.239.46']


@auto_switch_params()
def simple_params_name_return(network):
    return bitcoin.params.NAME


@mark.parametrize('network', networks)
def test_auto_switch_params_decorator(network):

    if network.name == 'bitcoin':
        assert simple_params_name_return(network) == 'mainnet'
    elif network.name == 'test-bitcoin':
        assert simple_params_name_return(network) == 'testnet'
    else:
        assert simple_params_name_return(network) == network.name

    bitcoin.SelectParams('mainnet')


@mark.parametrize('network', networks)
def test_get_network_obj_on_existing_networks(network):
    symbol = network.symbols[0]
    is_test_network = network.is_test_network()
    network_object = get_network_by_symbol(f"{symbol}{'-TESTNET' if is_test_network else ''}")

    assert type(network_object) == network
    assert network_object.symbols[0] == symbol
    assert network_object.is_test_network() == is_test_network


def test_get_network_obj_on_not_existing_network():
    assert get_network_by_symbol('NON_EXISTING_NETWORK_SYMBOL') is None


@mark.parametrize('network_symbol,address,is_valid', [
    ('LTC', 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq', True),
    ('BTC', '13iNsKgMfVJQaYVFqp5ojuudxKkVCMtkoa', True),
    ('MONA', 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ', True),
    ('LTC', '13iNsKgMfVJQaYVFqp5ojuudxKkVCMtkoa', False),
    ('LTC', '123', False),
    ('BTC', 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq', False),
    ('BTC', '123', False),
    ('BTC', '', False),
    ('BTC', 'non_hex_characters', False),

])
def test_valid_address(network_symbol, address, is_valid):
    network = get_network_by_symbol(network_symbol)
    assert network.is_valid_address(address) == is_valid


def test_broadcast_transaction(signed_transaction, connection_mock):
    btc_network = BitcoinTestNet()

    with connection_mock:
        assert signed_transaction.address == btc_network.broadcast_transaction(signed_transaction.raw_transaction)


def test_publish_transaction_from_network(signed_transaction, connection_mock):
    btc_network = BitcoinTestNet()

    with connection_mock:
        assert signed_transaction.address == btc_network.publish(signed_transaction.raw_transaction)


def test_publish_transaction_from_transaction(signed_transaction, connection_mock):
    with connection_mock:
        assert signed_transaction.address == signed_transaction.publish()


def test_deserialize_raw_transaction():
    valid_transaction = '0100000001350ff23c56027e3f7b8206d01a8fa2302d7ef82898e7ac795674a4e6450dd427000000008a47' \
                        '3044022033a4d693aedc99fea12d03acb07d3fbd2c26eb1da88df2820a2544058010a750022032195aaed8' \
                        'e773fa984bb3fe98ab138f6af36a500151f910a473f437bd63631501410402282aa6329ceada82ebcd53af' \
                        '7b1739cbc958e137ddde2b5da21183fa545b54cf75ce0c2296af902d53dd2a06fd783b7d8de00d74e612e8' \
                        '52bfee952d6744e70000000002a0e92f000000000017a914a2e40d94f0fa9d2bb8b6f424607f44a2e153da' \
                        '6f87c059693b000000001976a9143dfd3bba567574ba0508d01a96e89300af292b0688ac00000000'
    invalid_transaction = 'I am an invalid transaction :)'

    assert type(BitcoinTestNet.deserialize_raw_transaction(valid_transaction)) == CTransaction

    with raises(ImpossibleDeserialization):
        BitcoinTestNet.deserialize_raw_transaction(invalid_transaction)


def test_blockexplorer_tx_url():
    btc_network = BitcoinTestNet()
    url = btc_network.get_transaction_url('123')
    assert url.startswith('http')
    assert '123' in url


@patch('clove.network.bitcoin_based.monacoin.clove_req_json')
def test_extract_secret_monacoin(json_response):
    contract_transactions_mock = [
        'a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4',
        '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697'
    ]
    redeem_transaction_details = {
        'confirmed_height': 1304882,
        'hash': '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697',
        'hex': (
            '0100000001e4f0bb83bc3b52f921ad9d064768ba1702d9ec92befa3529a17e5163c90a11a000000000fd0001483045022100'
            'bf0dec5ab03d024147bc26df33a64f2389c4647fc1f9a92e93575cb5f2ff5081022060a54dd5135bc38eb6e75c65ec4e47ef'
            'a08e7298fed83757db31bd53619a17d501410447408e366d0e979101f776ab10753091b0b62ba9aa609d006263959e030fb2'
            'd96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1abb209a2cfc32611dbd3ac3261cd23622223e'
            '85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57646b3e056514185a97d15a7f086e8876a9141a376f66'
            '34e41c22b28bc9ef3336a623717083a46704ef6bdc5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac'
            '000000000160d36002000000001976a9141a376f6634e41c22b28bc9ef3336a623717083a488ac00000000'
        ),
        'locktime': 0,
        'size': 343,
        'txid': '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697',
        'version': 1,
        'vin': [{
            'address': 'PXGT7u4hd6gKYuzBkNUGsufYDARVAhoYue',
            'scriptSig': {
                'asm': (
                    '3045022100bf0dec5ab03d024147bc26df33a64f2389c4647fc1f9a92e93575cb5f2ff5081022060a54dd5135bc3'
                    '8eb6e75c65ec4e47efa08e7298fed83757db31bd53619a17d501 0447408e366d0e979101f776ab10753091b0b62'
                    'ba9aa609d006263959e030fb2d96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1abb '
                    '9a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2 OP_TRUE 63a61498ff8f419c576'
                    '46b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab1757'
                    '6a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac'
                ),
                'hex': (
                    '483045022100bf0dec5ab03d024147bc26df33a64f2389c4647fc1f9a92e93575cb5f2ff5081022060a54dd5135b'
                    'c38eb6e75c65ec4e47efa08e7298fed83757db31bd53619a17d501410447408e366d0e979101f776ab10753091b0'
                    'b62ba9aa609d006263959e030fb2d96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1a'
                    'bb209a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57'
                    '646b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab175'
                    '76a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac'
                )
            },
            'sequence': 0,
            'txid': 'a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4',
            'txinwitness': [],
            'value': 40000000,
            'vout': 0
        }],
        'vout': [{
            'n': 0,
            'scriptPubKey': {
                'address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
                'asm': 'OP_DUP OP_HASH160 1a376f6634e41c22b28bc9ef3336a623717083a4 OP_EQUALVERIFY OP_CHECKSIG',
                'hex': '76a9141a376f6634e41c22b28bc9ef3336a623717083a488ac',
                'type': 'pubkeyhash'
            },
            'value': 39900000
        }],
        'vsize': 343
    }
    json_response.side_effect = (contract_transactions_mock, redeem_transaction_details)
    monacoin = Monacoin()
    secret = monacoin.extract_secret_from_redeem_transaction(contract_address='PXGT7u4hd6gKYuzBkNUGsufYDARVAhoYue')
    assert secret == '9a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2'
