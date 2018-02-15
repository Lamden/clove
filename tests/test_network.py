from random import getrandbits
from unittest.mock import patch

import bitcoin
from bitcoin.messages import msg_getdata, msg_pong
import pytest
from pytest import mark
from validators import domain

from clove.network import __all__ as networks
from clove.network.base import BaseNetwork, auto_switch_params

seeds = [seed for network in networks for seed in network.seeds]


@mark.parametrize('network', networks)
def test_network_field_types(network):
    assert isinstance(network.name, str)
    assert isinstance(network.symbols, tuple)
    assert isinstance(network().default_symbol, str)
    assert isinstance(network.seeds, tuple)
    assert isinstance(network.port, int)
    assert isinstance(network.blacklist_nodes, dict)
    assert isinstance(network.message_start, bytes)
    assert isinstance(network.base58_prefixes, dict)


@mark.parametrize('seed', seeds)
def test_seeds_valid_dns_address(seed):
    assert domain(seed) is True


@mark.parametrize('network', networks)
@patch('urllib.request.urlopen')
def test_fee_per_kb_implementation(request_mock, network):
    if network.symbols[0] in ('BTC', 'LTC', 'DOGE', 'DASH') and not \
            (network.is_test_network() and network.name != 'test-bitcoin'):
        network.get_current_fee_per_kb()
    else:
        with pytest.raises(NotImplementedError):
            network.get_current_fee_per_kb()


def test_filter_blacklisted_nodes_method():
    network = BaseNetwork()
    network.blacklist_nodes = {'107.150.122.31': 4, '107.170.239.46': 1, '108.144.213.98': 3, '13.113.121.156': 4}
    nodes = list(network.blacklist_nodes.keys()) + ['34.207.248.232']
    assert network.filter_blacklisted_nodes(nodes) == ['34.207.248.232', '107.170.239.46', '108.144.213.98']
    assert network.filter_blacklisted_nodes(nodes, max_tries_number=2) == ['34.207.248.232', '107.170.239.46']


def test_extract_all_responses():
    bitcoin_network = networks[0]
    getdata = b'\xf9\xbe\xb4\xd9getdata\x00\x00\x00\x00\x00\x01\x00\x00\x00\x14\x06\xe0X\x00'
    pong = b'\xf9\xbe\xb4\xd9pong\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00~\xf0\xcab\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00'
    assert bitcoin_network.extract_all_responses(getdata) == [msg_getdata()]
    random_bytes = bytearray(getrandbits(8) for _ in range(10))
    assert bitcoin_network.extract_all_responses(getdata + random_bytes + pong) == [msg_getdata(), msg_pong()]
    assert bitcoin_network.extract_all_responses(b'') == [] == bitcoin_network.extract_all_responses(random_bytes)


@mark.parametrize('network', networks)
def test_symbol_mapping(network):
    is_test = network.is_test_network()
    symbol_mapping = network.get_symbol_mapping()
    assert symbol_mapping
    for (symbol, mapped_network) in symbol_mapping.items():
        assert issubclass(mapped_network, BaseNetwork)
        assert symbol in mapped_network.symbols
        assert mapped_network.is_test_network() == is_test


@mark.parametrize('network', networks)
def test_get_network_class_by_symbol(network):
    is_test = network.is_test_network()
    symbol_mapping = network.get_symbol_mapping()
    assert symbol_mapping
    for symbol in symbol_mapping:
        network_class = network.get_network_class_by_symbol(symbol)
        assert issubclass(network_class, BaseNetwork)
        assert symbol in network_class.symbols
        assert network_class.is_test_network() == is_test


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
