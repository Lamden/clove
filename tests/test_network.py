import ipaddress
from unittest.mock import patch

import bitcoin
from bitcoin.core import CTransaction
from pytest import mark, raises
from validators import domain

from clove.exceptions import ImpossibleDeserialization
from clove.network import BITCOIN_BASED as networks
from clove.network import BitcoinTestNet, ZCoin
from clove.network.bitcoin.base import BitcoinBaseNetwork
from clove.utils.bitcoin import auto_switch_params
from clove.utils.search import get_network_by_symbol


@mark.parametrize('network', networks)
def test_bitcoin_based_network_definitions(network):
    assert isinstance(network.API, bool)
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
    if network.bitcoin_based and network.API:
        assert isinstance(network.api_url, str)
    if network.blockexplorer_tx:
        assert isinstance(network.blockexplorer_tx, str)


def test_network_source_code_url_is_unique():
    mainnet_networks = [network for network in networks if not network.is_test_network()]
    source_code_urls_of_networks = set([network.source_code_url for network in mainnet_networks])
    assert len(mainnet_networks) == len(source_code_urls_of_networks)


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


@patch('clove.network.bitcoin.base.BitcoinBaseNetwork.broadcast_transaction')
def test_publish_transaction_from_network(broadcast_mock, signed_transaction):
    broadcast_mock.return_value = signed_transaction.address
    network = ZCoin()
    assert signed_transaction.address == network.publish(signed_transaction.raw_transaction)


@patch('clove.block_explorer.InsightAPIv4.publish')
def test_publish_transaction_from_transaction(publish_mock, signed_transaction):
    publish_mock.return_value = signed_transaction.address
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
