from pytest import mark
from validators import domain

from clove.network import __all__ as networks
from clove.utils.network import hostname_resolves

seeds = [seed for cls in networks for seed in cls.seeds]


@mark.parametrize('cls', networks)
def test_network_field_types(cls):
    assert isinstance(cls.name, str) is True
    assert isinstance(cls.symbols, tuple) is True
    assert isinstance(cls().default_symbol, str) is True
    assert isinstance(cls.seeds, tuple) is True
    assert isinstance(cls.port, int) is True


@mark.parametrize('seed', seeds)
def test_seeds_valid_dns_address(seed):
    assert domain(seed) is True


@mark.exclude_for_ci
@mark.parametrize('seed', seeds)
def test_seeds_dns_address_resolves_to_ip(seed):
    assert hostname_resolves(seed) is True
