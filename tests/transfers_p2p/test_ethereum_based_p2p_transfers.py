import pytest

from clove.network.base import BaseNetwork

'''''''''
Testing the Ethereum Network Base Class "p2p_transaction" method

'''
sender_address = '0xFa29E36A7eb4dBaE9ed93D803e5Bf95ae9772A27'
recipient_address = '0xE6425e2FB0Bc4AEb08b9c0358e4EaddB88Ea80Ad'
contract_address = '0xB347b9f5B56b431B2CF4e1d90a5995f7519ca792'

def test_p2p_transaction_object(infura_token):
    '''
    Transaction Object can be created
    '''
    network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
    transaction_value = 0.0
    assert network.transaction_p2p(sender_address, recipient_address, transaction_value) is not None

def test_p2p_transaction_token_object(infura_token):
    '''
    Token Transaction Object can be created
    '''
    transaction_value = 0.0
    network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
    assert network.transaction_p2p(sender_address, recipient_address, transaction_value, contract_address) is not None

def test_p2p_transaction_token_decimals(infura_token):
    '''
    Value has too many decimals
    '''
    with pytest.raises(ValueError) as error:
        network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
        transaction_value = 0.1
        Zeenus_contract = '0x1f9061B953bBa0E36BF50F21876132DcF276fC6e'
        network.transaction_p2p(sender_address, recipient_address, transaction_value, Zeenus_contract)
    assert str(error.value) == ('Zeenus 💪 token supports at most 0 decimal places.')

def test_p2p_transaction_sender_AssertionError(infura_token):
    '''
    Produced a AssertionError when sender_address the incorrect ethereum format
    '''
    with pytest.raises(AssertionError) as error:
        network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
        transaction_value = 0.0
        bad_sender_address = "badaddress"
        network.transaction_p2p(bad_sender_address, recipient_address, transaction_value, contract_address)
    assert str(error.value) == ('Provided address is not properly formatted.') 

def test_p2p_transaction_recipient_AssertionError(infura_token):
    '''
    Produced a AssertionError when recipient_address the incorrect ethereum format
    '''
    with pytest.raises(AssertionError) as error:
        network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
        transaction_value = 0.0
        bad_recipient_address = "badaddress"
        network.transaction_p2p(sender_address, bad_recipient_address, transaction_value, contract_address)
    assert str(error.value) == ('Provided address is not properly formatted.') 

def test_p2p_transaction_value_TypeError(infura_token):
    '''
    Produces a TypeError if the transaction value is not INT
    '''
    with pytest.raises(TypeError) as error:
        network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
        transaction_value = 'testingnotINT'
        network.transaction_p2p(sender_address, recipient_address, transaction_value, contract_address)
    assert str(error.value) == ('Transaction value must be a Number') 

def test_p2p_transaction_sender_TypeError(infura_token):
    '''
    Produces a TypeError if the sender_address is not STR
    '''
    with pytest.raises(TypeError) as error:
        network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
        transaction_value = 0.0
        bad_sender_address = 2
        network.transaction_p2p(bad_sender_address, recipient_address, transaction_value, contract_address)
    assert str(error.value) == ('sender_address must be STR')

def test_p2p_transaction_recipient_TypeError(infura_token):
    '''
    Produces a TypeError if the recipient_address is not STR
    '''
    with pytest.raises(TypeError) as error:
        network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
        transaction_value = 0.0
        bad_recipient_address = 2
        network.transaction_p2p(sender_address, bad_recipient_address, transaction_value, contract_address)
    assert str(error.value) == ('recipient_address must be STR') 

def test_p2p_transaction_contract_TypeError(infura_token):
    '''
    Produces a TypeError if the contract_address is not STR
    '''
    with pytest.raises(TypeError) as error:
        network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
        transaction_value = 0.0
        bad_contract_address = 2
        network.transaction_p2p(sender_address, recipient_address, transaction_value, bad_contract_address)
    assert str(error.value) == ('token_address must be STR') 


'''''''''
ETH Tests
Test creating and signing transaction objects
'''
def test_p2p_transaction_sign_tx_ETH(infura_token):
    '''
    ETH Transaction transaction can be signed
    '''
    network = BaseNetwork.get_network_by_symbol('ETH')
    p2p_transaction = network.transaction_p2p('0x424638050A2b9984030954C8A19E2032beb11D48', '0x424638050A2b9984030954C8A19E2032beb11D48', 0.001)
    p2p_transaction.sign( 'FCD906EEC6D9710E545A5DFE12BC1C5D1143F02C7340C8031DA668769615F49F' )
    assert type( p2p_transaction.raw_transaction ) is str

def test_p2p_transaction_token_sign_tx_ETH(infura_token):
    '''
    ETH Token Transaction unsigned transaction can be created
    '''
    network = BaseNetwork.get_network_by_symbol('ETH')
    TAU_contract = '0xc27A2F05fa577a83BA0fDb4c38443c0718356501'
    p2p_transaction = network.transaction_p2p('0x424638050A2b9984030954C8A19E2032beb11D48', '0x424638050A2b9984030954C8A19E2032beb11D48', 0.001, TAU_contract)
    p2p_transaction.sign( 'FCD906EEC6D9710E545A5DFE12BC1C5D1143F02C7340C8031DA668769615F49F' )
    assert type( p2p_transaction.raw_transaction ) is str

'''''''''
ETH-TESTNET Tests
Test creating and signing transaction objects
'''
def test_p2p_transaction_sign_tx_ETH_Testnet(infura_token):
    '''
    ETH-TESTNET Transaction transaction can be signed
    '''
    network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
    p2p_transaction = network.transaction_p2p('0xFa29E36A7eb4dBaE9ed93D803e5Bf95ae9772A27', '0xFa29E36A7eb4dBaE9ed93D803e5Bf95ae9772A27', 0.001)
    p2p_transaction.sign( 'FCD906EEC6D9710E545A5DFE12BC1C5D1143F02C7340C8031DA668769615F49F' )
    assert type( p2p_transaction.raw_transaction ) is str

def test_p2p_transaction_token_sign_tx_ETH_Testnet(infura_token):
    '''
    ETH-TESTNET Token Transaction unsigned transaction can be created
    '''
    network = BaseNetwork.get_network_by_symbol('ETH-TESTNET')
    POLY_contract = '0xB347b9f5B56b431B2CF4e1d90a5995f7519ca792'
    p2p_transaction = network.transaction_p2p('0xFa29E36A7eb4dBaE9ed93D803e5Bf95ae9772A27', '0xFa29E36A7eb4dBaE9ed93D803e5Bf95ae9772A27', 0.001, POLY_contract)
    p2p_transaction.sign( 'FCD906EEC6D9710E545A5DFE12BC1C5D1143F02C7340C8031DA668769615F49F' )
    assert type( p2p_transaction.raw_transaction ) is str

'''''''''
MUSIC COIN WEB3 PROVIDER DOWN
Music Coin Tests
Test creating and signing transaction objects

def test_p2p_transaction_sign_tx_MUSIC():

    'MUSIC Transaction transaction can be signed

    network = BaseNetwork.get_network_by_symbol('MUSIC')
    p2p_transaction = network.transaction_p2p('0x02e3e151755ef1ffa83f90166e378ebaa102d698', '0x02e3e151755ef1ffa83f90166e378ebaa102d698', 0.001)
    p2p_transaction.sign( 'FCD906EEC6D9710E545A5DFE12BC1C5D1143F02C7340C8031DA668769615F49F' )
    assert type( p2p_transaction.raw_transaction ) is str
'''

'''''''''
EtherGem Tests
Test creating and signing transaction objects
'''
def test_p2p_transaction_sign_tx_EGEM():
    '''
    EGEM Transaction transaction can be signed
    '''
    network = BaseNetwork.get_network_by_symbol('EGEM')
    p2p_transaction = network.transaction_p2p('0xa4191f0bafb95717fd91feffb517cd1017a67a14', '0xa4191f0bafb95717fd91feffb517cd1017a67a14', 0.001)
    p2p_transaction.sign( 'FCD906EEC6D9710E545A5DFE12BC1C5D1143F02C7340C8031DA668769615F49F' )
    assert type( p2p_transaction.raw_transaction ) is str