from collections import namedtuple
from contextlib import contextmanager
from io import BytesIO
import os
from unittest.mock import MagicMock, patch

from bitcoin.messages import msg_getdata, msg_reject, msg_verack, msg_version
from eth_abi import encode_abi
from hexbytes import HexBytes
import pytest

from .constants import abi_swaps_types, non_zero_balance_abi_contract

from clove.network.bitcoin import BitcoinTestNet
from clove.network.bitcoin.utxo import Utxo

Key = namedtuple('Key', ['secret', 'address'])


def pytest_addoption(parser):
	parser.addoption('--CRYPTOID_API_KEY', metavar='CRYPTOID_API_KEY', default=None, help='specify resolution cryptoID API KEY"')
	parser.addoption('--INFURA_TOKEN', metavar='INFURA_TOKEN', default=None, help='specify resolution infura token API KEY"')

@pytest.fixture
def alice_wallet():
    return BitcoinTestNet.get_wallet(private_key='cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe')


@pytest.fixture
def bob_wallet():
    return BitcoinTestNet.get_wallet(private_key='cRoFBWMvcLXrLsYFt794NRBEPUgMLf5AmnJ7VQwiEenc34z7zSpK')


@pytest.fixture
def alice_utxo(alice_wallet):
    return [
        Utxo(
            tx_id='6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8',
            vout=1,
            value=0.78956946,
            tx_script='76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac',
            wallet=alice_wallet
        ),
    ]


@pytest.fixture
def bob_utxo(bob_wallet):
    return [
        Utxo(
            tx_id='56384654b9e21242588c8fa5f905808a96039a8e1257312f35e0b06c55fa19fb',
            vout=1,
            value=0.87961162,
            tx_script='76a9143f8870a5633e4fdac612fba47525fef082bbe96188ac',
            wallet=bob_wallet
        ),
    ]


@pytest.fixture
def unsigned_transaction(alice_wallet, bob_wallet, alice_utxo):
    btc_network = BitcoinTestNet()
    transaction = btc_network.atomic_swap(
        alice_wallet.address,
        bob_wallet.address,
        0.7,
        alice_utxo
    )
    return transaction


@pytest.fixture
def signed_transaction(unsigned_transaction):
    transaction = unsigned_transaction
    transaction.fee_per_kb = 0.002
    transaction.add_fee_and_sign()
    return transaction


@pytest.fixture
def btc_testnet_contract(signed_transaction):
    network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()
    return network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )


@contextmanager
@pytest.fixture
def connection_mock(signed_transaction):
    connection = MagicMock()

    connection.getsockname.return_value = ('127.0.0.1', 8800)
    connection.getpeername.return_value = ('127.0.0.1', 8800)
    connection.getpeername.return_value = ('127.0.0.1', 8800)

    protocol_version = 6002
    version = msg_version(protocol_version).to_bytes()
    verack = msg_verack(protocol_version).to_bytes()

    getdata = msg_getdata(protocol_version)
    getdata = getdata.msg_deser(BytesIO(b'\x01\x01\x00\x00\x00' + signed_transaction.tx.GetHash())).to_bytes()

    connection.recv.side_effect = (
        version + verack,
        getdata,
    )

    capture = BitcoinTestNet.capture_messages

    def capture_messages_mock(*args, **kwargs):
        if msg_reject in args[1]:
            return None
        else:
            return capture(*args, **kwargs)

    with patch('socket.create_connection', return_value=connection):
        with patch('socket.gethostbyname_ex', return_value=(None, None, ['127.0.0.1'])):
            with patch.object(BitcoinTestNet, 'capture_messages', new=capture_messages_mock):
                yield


def web3_request_side_effect(method, params):
    if method == 'eth_gasPrice':
        return 20000000000
    elif method == 'eth_estimateGas':
        return 125000
    elif method == 'eth_getTransactionCount':
        return 1
    elif method == 'net_version':
        return 42
    elif method == 'eth_blockNumber':
        return 8400000
    elif method == 'eth_call':
        encoded_abi = encode_abi(abi_swaps_types, non_zero_balance_abi_contract)
        return encoded_abi.hex()
    elif method == 'eth_getFilterLogs':
        return [
            {
                'data': '0xbc2424e1dcdd2e425c555bcea35a54fd27cf540e60f18366e153e3fb7cf4490c',
                'transactionHash': HexBytes('0x65320e57b9d18ec08388896b029ad1495beb7a57c547440253a1dde01b4485f1'),
            }
        ]
    return None


@pytest.fixture
def web3_request_mock():
    with patch('web3.manager.RequestManager.request_blocking', side_effect=web3_request_side_effect):
        yield


@pytest.fixture
def infura_token(request):
    os.environ['INFURA_TOKEN'] = request.config.getoption('--INFURA_TOKEN')
    yield
    del os.environ['INFURA_TOKEN']

@pytest.fixture
def etherscan_token():
    os.environ['ETHERSCAN_API_KEY'] = 'PRF1ZEGKUDN9P2WKITCCYRU9E3ASPKGBKZ'
    yield
    del os.environ['ETHERSCAN_API_KEY']

@pytest.fixture
def cryptoid_token(request):
    os.environ['CRYPTOID_API_KEY'] = request.config.getoption('--CRYPTOID_API_KEY')
    yield
    del os.environ['CRYPTOID_API_KEY']

@pytest.fixture
def fake_cryptoid_token():
    os.environ['CRYPTOID_API_KEY'] = '123'
    yield
    del os.environ['CRYPTOID_API_KEY']
