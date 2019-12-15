import pytest

from clove.network.base import BaseNetwork

def test_unsupported_network():
    expected = 'network is not supported.'
    with pytest.raises(RuntimeError, message=expected):
        BaseNetwork.get_network_by_symbol('TESTING')

def test_bad_address_insight():
    network = BaseNetwork.get_network_by_symbol('BTC')
    assert network.get_balance('BadAddress') is 0

def test_bad_address_cryptoID(cryptoid_token):
    network = BaseNetwork.get_network_by_symbol('LTC')
    assert network.get_balance('BadAddress') is None
        
def test_bad_address_format_web3(infura_token):
    network = BaseNetwork.get_network_by_symbol('ETH')
    expected = 'Provided address is not properly formatted.'
    with pytest.raises(AssertionError, message=expected):
        network.get_balance('BadAddress')

def test_bad_address_invalid_web3(infura_token):
    network = BaseNetwork.get_network_by_symbol('ETH')
    expected = "invalid literal for int() with base 16: '0x49d77B4a97fBEdFaA9526BDbE00Ac0f0859aB91g"
    with pytest.raises(ValueError, message=expected):
        network.get_balance('0x49d77B4a97fBEdFaA9526BDbE00Ac0f0859aB91g')

def test_bad_contractaddress_format_web3(infura_token):
    network = BaseNetwork.get_network_by_symbol('ETH')
    expected = 'Provided address is not properly formatted.'
    with pytest.raises(AssertionError, message=expected):
        network.get_balance('0x49d77B4a97fBEdFaA9526BDbE00Ac0f0859aB91f', 'BadAddress')

def test_bad_contractaddress_invalid_web3(infura_token):
    network = BaseNetwork.get_network_by_symbol('ETH')
    expected = "invalid literal for int() with base 16: 0xc27a2f05fa577a83bthiscontractdoesntexist"
    with pytest.raises(ValueError, message=expected):
        network.get_balance('0x49d77B4a97fBEdFaA9526BDbE00Ac0f0859aB91f', '0xc27a2f05fa577a83bthiscontractdoesntexist')