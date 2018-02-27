from unittest.mock import patch

import bitcoin
import pytest
from pytest import mark
from validators import domain

from clove.constants import API_SUPPORTED_NETWORKS
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
@patch('clove.network.base.get_last_transactions', return_value=['aaa', 'bbb', 'ccc'])
@patch('clove.network.base.get_transaction_size', side_effect=[200, 300, 700])
@patch('clove.network.base.get_transaction_fee', side_effect=[0.02, 0.03, 0.07])
def test_fee_per_kb_implementation(fee_mock, size_mock, transactions_mock, network):
    if network.name in ('test-bitcoin', 'dogecoin'):
        return
    if network.is_test_network() or network.symbols[0].lower() not in API_SUPPORTED_NETWORKS:
        with pytest.raises(NotImplementedError):
            network.get_current_fee_per_kb()
    else:
        assert network.get_current_fee_per_kb() == 0.1


def test_filter_blacklisted_nodes_method():
    network = BaseNetwork()
    network.blacklist_nodes = {'107.150.122.31': 4, '107.170.239.46': 1, '108.144.213.98': 3, '13.113.121.156': 4}
    nodes = list(network.blacklist_nodes.keys()) + ['34.207.248.232']
    assert network.filter_blacklisted_nodes(nodes) == ['34.207.248.232', '107.170.239.46', '108.144.213.98']
    assert network.filter_blacklisted_nodes(nodes, max_tries_number=2) == ['34.207.248.232', '107.170.239.46']


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
