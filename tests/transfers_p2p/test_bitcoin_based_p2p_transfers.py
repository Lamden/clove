from clove.network.base import BaseNetwork
import pytest

'''''''''
Testing the Bitcoin Network Base Class "p2p_transaction" method

'''
sender_address = 'mweQsmD7SZs7Kk49XoReDrXFmxyrxaE8wK'
recipient_address = 'mgB3NHwQFdSA4AKtpXqNvnUwQQbM3DojTm'

BTCTESTnetwork = BaseNetwork.get_network_by_symbol('BTC-TESTNET')

def test_p2p_transaction_object():
    '''
    Transaction Object can be created
    '''
    transaction_value = 0.0
    assert BTCTESTnetwork.transaction_p2p(sender_address, recipient_address, transaction_value) is not None

def test_p2p_transaction_value_ValueError():
    '''
    Produces a ValueError if there are not enough UTXOs to make up the transfer value
    '''
    with pytest.raises(ValueError) as error:
        transaction_value = 1.0
        BTCTESTnetwork.transaction_p2p(sender_address, recipient_address, transaction_value)
    assert str(error.value) == 'Cannot find enough UTXO\'s. Found 0.01003237 of 1.00000000'   

def test_p2p_transaction_sender_AttributeError():
    '''
    Produces a AttributeError if the no UTXO's could be found for the sender_address
    '''
    with pytest.raises(AttributeError) as error:
        transaction_value = 0.0
        bad_sender_address = 'notanaddress'
        BTCTESTnetwork.transaction_p2p(bad_sender_address, recipient_address, transaction_value)
    assert str(error.value) == (f'Cannot get UTXO\'s for address {bad_sender_address}')

def test_p2p_transaction_recipient_ValueError():
    '''
    Produces a ValueError if the recipient_address is not proper bitcoin format
    '''
    with pytest.raises(ValueError) as error:
        transaction_value = 0.0
        bad_recipient_address = 'thisisabadaddress'
        BTCTESTnetwork.transaction_p2p(sender_address, bad_recipient_address, transaction_value)
    assert str(error.value) == ('Given recipient address is invalid.') 

def test_p2p_transaction_value_TypeError():
    '''
    Produces a TypeError if the transaction value is not INT
    '''
    with pytest.raises(TypeError) as error:
        transaction_value = 'testingnotINT'
        BTCTESTnetwork.transaction_p2p(sender_address, recipient_address, transaction_value)
    assert str(error.value) == ('Transaction value must be a Number') 

def test_p2p_transaction_sender_TypeError():
    '''
    Produces a TypeError if the sender_address is not STR
    '''
    with pytest.raises(TypeError) as error:
        transaction_value = 0.0
        bad_sender_address = 2
        BTCTESTnetwork.transaction_p2p(bad_sender_address, recipient_address, transaction_value)
    assert str(error.value) == ('sender_address must be STR')

def test_p2p_transaction_recipient_TypeError():
    '''
    Produces a TypeError if the recipient_address is not STR
    '''
    with pytest.raises(TypeError) as error:
        transaction_value = 0.0
        bad_recipient_address = 2
        BTCTESTnetwork.transaction_p2p(sender_address, bad_recipient_address, transaction_value)
    assert str(error.value) == ('recipient_address must be STR') 


'''''''''
Bitcoin Based Tests
  - This will test that utxo objects can be obtained for all supported coins which will create the transaction object
  - Then it will test to make sure that an unsigned transaction can be created
'''
### InsiteAPI based coins ###

#Bitcoin (BTC)
def test_p2p_transaction_BTC():
    '''
    BTC Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('BTC')
    p2p_transaction = network.transaction_p2p('12c35gMcjsEidhufU9Pazg888HHjfJzjxQ', '12c35gMcjsEidhufU9Pazg888HHjfJzjxQ', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Bitcoin Test Net (BTC-TESTNET)
def test_p2p_transaction_BTC_TESTNET():
    '''
    BTC-TESTNET Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('BTC-TESTNET')
    p2p_transaction = network.transaction_p2p('n31RX4xTyvfJ1GubXCMWLRCrxa5UkZByrC', 'n31RX4xTyvfJ1GubXCMWLRCrxa5UkZByrC', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Bitcoin Cash (BCH)
def test_p2p_transaction_BCH():
    '''
    BCH Transaction Object can be created as well as unsigned transaction
        ** only works with BCH legacy addresses
    '''
    network = BaseNetwork.get_network_by_symbol('BCH')
    p2p_transaction = network.transaction_p2p('14719bzrTyMvEPcr7ouv9R8utncL9fKJyf', '14719bzrTyMvEPcr7ouv9R8utncL9fKJyf', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Bitcoin Gold (BTG)
def test_p2p_transaction_BTG():
    '''
    BTG Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('BTG')
    p2p_transaction = network.transaction_p2p('GVK4S5HHMBcEbATd1Hgiv5wgRKvbFyJaSe', 'GVK4S5HHMBcEbATd1Hgiv5wgRKvbFyJaSe', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Mono (MONA)
def test_p2p_transaction_MONA():
    '''
    MONA Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('MONA')
    p2p_transaction = network.transaction_p2p('MLfcYkhxiDecXqEim8jL8Rq52ZUVmMo8sT', 'MLfcYkhxiDecXqEim8jL8Rq52ZUVmMo8sT', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Ravencoin (RVN)
def test_p2p_transaction_RVN():
    '''
    RVN Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('RVN')
    p2p_transaction = network.transaction_p2p('RHwb533S2BRL3ac8L872hXKLHsrE94fcrk', 'RHwb533S2BRL3ac8L872hXKLHsrE94fcrk', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Ravencoin TEST-NET (RVN-TESTNET)
def test_p2p_transaction_RVN_TESTNET():
    '''
    RVN-TESTNET Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('RVN-TESTNET')
    p2p_transaction = network.transaction_p2p('mzeGFKD9Zs7oH2WwAkqCm1uewJg2j2urDs', 'mzeGFKD9Zs7oH2WwAkqCm1uewJg2j2urDs', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

### CryptoID API based coins ###

#Dash (DASH)
def test_p2p_transaction_BTC_DASH():
    '''
    DASH Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('DASH')
    p2p_transaction = network.transaction_p2p('XccPicDbg7HhRfFwPU3Z2CFVpHSYAhuxtu', 'XccPicDbg7HhRfFwPU3Z2CFVpHSYAhuxtu', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Digibyte (DGB)
def test_p2p_transaction_DGB():
    '''
    DGB Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('DGB')
    p2p_transaction = network.transaction_p2p('D7CWTxvtwM2216a7aRGyYuqAEQDaudXA5k', 'D7CWTxvtwM2216a7aRGyYuqAEQDaudXA5k', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None

#Litecoin (LTC)
def test_p2p_transaction_LTC():
    '''
    LTC Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('LTC')
    p2p_transaction = network.transaction_p2p('LVmMhqp6JDTTknTqLWGhXvboXyron6zkKB', 'LVmMhqp6JDTTknTqLWGhXvboXyron6zkKB', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None
    
#ZCoin (XZC)
def test_p2p_transaction_XZC():
    '''
    XZC Transaction Object can be created as well as unsigned transaction
    '''
    network = BaseNetwork.get_network_by_symbol('XZC')
    p2p_transaction = network.transaction_p2p('aK6RS6dMf3xRGg9DF2JA3ExMfcDWXL4Zyp', 'aK6RS6dMf3xRGg9DF2JA3ExMfcDWXL4Zyp', 0)
    assert p2p_transaction is not None
    assert p2p_transaction.create_unsigned_transaction is not None