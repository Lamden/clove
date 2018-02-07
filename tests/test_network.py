from random import getrandbits
from unittest.mock import patch

from bitcoin.messages import msg_getdata, msg_pong
import pytest
from pytest import mark
from validators import domain

from clove.network import __all__ as networks
from clove.network.base import BaseNetwork
from clove.utils.network import hostname_resolves

seeds = [seed for network in networks for seed in network.seeds]


@mark.parametrize('network', networks)
def test_network_field_types(network):
    assert isinstance(network.name, str)
    assert isinstance(network.symbols, tuple)
    assert isinstance(network().default_symbol, str)
    assert isinstance(network.seeds, tuple)
    assert isinstance(network.port, int)
    assert isinstance(network.blacklist_nodes, dict)


@mark.parametrize('seed', seeds)
def test_seeds_valid_dns_address(seed):
    assert domain(seed) is True


@mark.exclude_for_ci
@mark.parametrize('seed', seeds)
def test_seeds_dns_address_resolves_to_ip(seed):
    assert hostname_resolves(seed) is True


@mark.parametrize('network', networks)
@patch('urllib.request.urlopen')
def test_fee_per_kb_implementation(request_mock, network):
    if network.symbols[0] in ('BTC', 'LTC', 'DOGE', 'DASH') and not network.name.startswith('test-'):
        network.get_current_fee_per_kb()
    else:
        with pytest.raises(NotImplementedError):
            network.get_current_fee_per_kb()


def test_filter_blacklisted_nodes_method():
    network = BaseNetwork()
    network.blacklist_nodes = {'107.150.122.31': 4, '107.170.239.46': 1, '108.144.213.98': 3, '13.113.121.156': 4}
    nodes = list(network.blacklist_nodes.keys()) + ['34.207.248.232']
    assert network.filter_blacklisted_nodes(nodes) == ['107.170.239.46', '108.144.213.98', '34.207.248.232']
    assert network.filter_blacklisted_nodes(nodes, max_tries_number=2) == ['107.170.239.46', '34.207.248.232']


def test_extract_all_the_responses():
    getdata = b'\xf9\xbe\xb4\xd9getdata\x00\x00\x00\x00\x00\x01\x00\x00\x00\x14\x06\xe0X\x00'
    pong = b'\xf9\xbe\xb4\xd9pong\x00\x00\x00\x00\x00\x00\x00\x00\x08\x00\x00\x00~\xf0\xcab\x00' \
           b'\x00\x00\x00\x00\x00\x00\x00'
    assert BaseNetwork.extract_all_the_responses(getdata) == [msg_getdata()]
    random_bytes = bytearray(getrandbits(8) for _ in range(10))
    assert BaseNetwork.extract_all_the_responses(getdata + random_bytes + pong) == [msg_getdata(), msg_pong()]
    assert BaseNetwork.extract_all_the_responses(b'') == [] == BaseNetwork.extract_all_the_responses(random_bytes)
