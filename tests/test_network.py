from unittest.mock import patch

import pytest
from pytest import mark
from validators import domain

from clove.network import __all__ as networks
from clove.utils.network import hostname_resolves

seeds = [seed for network in networks for seed in network.seeds]


@mark.parametrize('network', networks)
def test_network_field_types(network):
    assert isinstance(network.name, str) is True
    assert isinstance(network.symbols, tuple) is True
    assert isinstance(network().default_symbol, str) is True
    assert isinstance(network.seeds, tuple) is True
    assert isinstance(network.port, int) is True


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
