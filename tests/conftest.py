from collections import namedtuple
from contextlib import contextmanager
from io import BytesIO
import os
from unittest.mock import MagicMock, patch

from bitcoin.messages import msg_getdata, msg_reject, msg_verack, msg_version
from hexbytes.main import HexBytes
import pytest
from web3.utils.datastructures import AttributeDict

from clove.network.bitcoin import BitcoinTestNet
from clove.network.bitcoin.utxo import Utxo

Key = namedtuple('Key', ['secret', 'address'])


eth_initial_transaction = AttributeDict({
    'blockHash': HexBytes('0xebb8d4e62dc5b0732bee6e2c3946c5a972988f41fbac321eb73311930a936804'),
    'blockNumber': 6600435,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'gas': 126221,
    'gasPrice': 14959965017,
    'hash': HexBytes('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41'),
    'input': (
        '0xeb8ae1ed000000000000000000000000000000000000000000000000000000005abe25ea10ff9'
        '72f3d8181f603aa7f6b4bc172de730fec2b00000000000000000000000000000000000000000000'
        '0000d867f293ba129629a9f9355fa285b8d3711a9092'
    ),
    'nonce': 16,
    'publicKey': HexBytes(
        '0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adcb150e521'
        '6213bc301f3a6b71a178c81ddd34a361d696c8cb03970590d4f'
    ),
    'r': HexBytes('0x7a4e11ea96640fb0ab255960cea6afcf16732246ce1dadeec52eb6a8d59c2e05'),
    'raw': HexBytes(
        '0xf8ca1085037baef3598301ed0d949f7e5402ed0858ea0c5914d44b900a42c89547b80cb864eb8'
        'ae1ed000000000000000000000000000000000000000000000000000000005abe25ea10ff972f3d'
        '8181f603aa7f6b4bc172de730fec2b000000000000000000000000000000000000000000000000d'
        '867f293ba129629a9f9355fa285b8d3711a90921ba07a4e11ea96640fb0ab255960cea6afcf1673'
        '2246ce1dadeec52eb6a8d59c2e05a06f47ffe2bc88915013295be61c503bc52762fe4f7826fa249'
        '0b2d302a11bff85'
    ),
    's': HexBytes('0x6f47ffe2bc88915013295be61c503bc52762fe4f7826fa2490b2d302a11bff85'),
    'standardV': 0,
    'to': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'transactionIndex': 0,
    'v': 27,
    'value': 12
})

eth_unsupported_transaction = AttributeDict({
    'input': (
        '0xeb7ae1ed000000000000000000000000000000000000000000000000000000005abe25ea10ff9'
        '72f3d8181f603aa7f6b4bc172de730fec2b00000000000000000000000000000000000000000000'
        '0000d867f293ba129629a9f9355fa285b8d3711a9092'
    ),
})

eth_redeem_tranaction = AttributeDict({
    'blockHash': HexBytes('0x4a1f01ed71161e103d0fc4a82ec2facdc1b685e3a597fca07bb9b822b74ed686'),
    'blockNumber': 6612187,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'gas': 100000,
    'gasPrice': 1000000000,
    'hash': HexBytes('0x89b0d28e93ce55da4adab989cd48a524402eb154b23e1777f82e715589aba317'),
    'input': '0xeda1122c1e5a567ab04cc900c3da01d1b61c1a3755d648410963c3d0767ed2e0138e03a1',
    'nonce': 14,
    'publicKey': HexBytes(
        '0x579c6126677857d4d5a227ed47efbd9742e26f60449e8ea6a536c0dd9b2fb6f'
        'b14e0fddc7cb06fd78d2c6c3ef4d1b72e488096504817ed7ac252b2453cbfab56'
    ),
    'r': HexBytes('0x9ca27c2d31c663c0202851eea34e39b90311173916101bf3c3437f0fa23e54e9'),
    'raw': HexBytes(
        '0xf8880e843b9aca00830186a0949f7e5402ed0858ea0c5914d44b900a42c8954'
        '7b880a4eda1122c1e5a567ab04cc900c3da01d1b61c1a3755d648410963c3d076'
        '7ed2e0138e03a11ca09ca27c2d31c663c0202851eea34e39b90311173916101bf'
        '3c3437f0fa23e54e9a022ae2c66a04f526f17d6cbb2bf873fbbb5c3bf68bfdebf'
        'd08fbdd2b9088283a0'
    ),
    's': HexBytes('0x22ae2c66a04f526f17d6cbb2bf873fbbb5c3bf68bfdebfd08fbdd2b9088283a0'),
    'standardV': 1,
    'to': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'transactionIndex': 3,
    'v': 28,
    'value': 0,
})

token_initial_transaction = AttributeDict({
    'blockHash': HexBytes('0x2d10ee8f6d5b809cdcd52994a5d80829b3b431ac2353abd09905c144304e6c24'),
    'blockNumber': 6632638,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'gas': 1000000,
    'gasPrice': 2000000000,
    'hash': HexBytes('0x316d3aaa252adb025c3486cf83949245f3f10edc169e1eb0772ed074fddb8be6'),
    'input': '0x52f50db700000000000000000000000000000000000000000000000000000000'
             '5ac0e7e406821b98736162c1b007155e818536ec5fd57950000000000000000000'
             '000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a'
             '909200000000000000000000000053e546387a0d054e7ff127923254c0a679da6d'
             'bf0000000000000000000000000000000000000000000000000000000000000064',
    'nonce': 25,
    'publicKey': HexBytes(
        '0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adc'
        'b150e5216213bc301f3a6b71a178c81ddd34a361d696c8cb03970590d4f'
    ),
    'r': HexBytes('0x5d66dc1d458dc78eaa639fe425143f21a09706ede02415b7fd41a7bbb88c4da0'),
    'raw': HexBytes(
        '0xf90109198477359400830f4240947657ca877fac31d20528b473162e39b6e152fd2e80b8a452'
        'f50db7000000000000000000000000000000000000000000000000000000005ac0e7e406821b98'
        '736162c1b007155e818536ec5fd579500000000000000000000000000000000000000000000000'
        '00d867f293ba129629a9f9355fa285b8d3711a909200000000000000000000000053e546387a0d'
        '054e7ff127923254c0a679da6dbf00000000000000000000000000000000000000000000000000'
        '000000000000641ca05d66dc1d458dc78eaa639fe425143f21a09706ede02415b7fd41a7bbb88c'
        '4da0a07d2ceb71a0965ea61bcafbe86670f58c3b157d8dff456b3bca195f3d2c57d595'
    ),
    's': HexBytes('0x7d2ceb71a0965ea61bcafbe86670f58c3b157d8dff456b3bca195f3d2c57d595'),
    'standardV': 1,
    'to': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
    'transactionIndex': 0,
    'v': 28,
    'value': 0
})


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
    return None


@pytest.fixture
def web3_request_mock():
    with patch('web3.manager.RequestManager.request_blocking', side_effect=web3_request_side_effect):
        yield


@pytest.fixture
def infura_token():
    os.environ['INFURA_TOKEN'] = 'WsUXSFPvO9t86xDAAhNi'
    yield
    del os.environ['INFURA_TOKEN']


@pytest.fixture
def etherscan_token():
    os.environ['ETHERSCAN_API_KEY'] = 'PRF1ZEGKUDN9P2WKITCCYRU9E3ASPKGBKZ'
    yield
    del os.environ['ETHERSCAN_API_KEY']


@pytest.fixture
@patch('clove.utils.external_source.clove_req_json')
def etherscan_api_response(etherscan_api_mock):
    etherscan_api_mock.return_value = {
        "message": "OK",
        "result": [
            {
                "blockNumber": "6628836",
                "contractAddress": "",
                "errCode": "",
                "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
                "gas": "2300",
                "gasUsed": "0",
                "hash": "0x862b393fd64d4c1ae1a6cc55f2c6f36a87fdce46dcc7abb1a7ba174c10bb0281",
                "input": "",
                "isError": "0",
                "timeStamp": "1522398684",
                "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
                "traceId": "0",
                "type": "call",
                "value": "8"
            },
            {
                "blockNumber": "6712309",
                "contractAddress": "",
                "errCode": "",
                "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
                "gas": "2300",
                "gasUsed": "0",
                "hash": "0x2dd60f28a3ef781fd12adfeb3b622fe424a268816392bbac4d5116ead94a0fde",
                "input": "",
                "isError": "0",
                "timeStamp": "1522841088",
                "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
                "traceId": "0",
                "type": "call",
                "value": "1"
            },
            {
                "blockNumber": "6793058",
                "contractAddress": "",
                "errCode": "",
                "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
                "gas": "2300",
                "gasUsed": "0",
                "hash": "0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1",
                "input": "",
                "isError": "0",
                "timeStamp": "1523275524",
                "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
                "traceId": "0",
                "type": "call",
                "value": "500000000000000000"
            },
            {
                "blockNumber": "6795065",
                "contractAddress": "",
                "errCode": "",
                "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
                "gas": "2300",
                "gasUsed": "0",
                "hash": "0x4c21cf7bb5d64f659ba02f84e9af42150d7911147588a2b5fe4330f73d6afb33",
                "input": "",
                "isError": "0",
                "timeStamp": "1523285852",
                "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
                "traceId": "0",
                "type": "call",
                "value": "9"
            },
            {
                "blockNumber": "6837685",
                "contractAddress": "",
                "errCode": "",
                "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
                "gas": "2300",
                "gasUsed": "0",
                "hash": "0xbf0b86b80ca9780c7e992c9c5bf5fc8db75e434821fc0a51545e469f554f9878",
                "input": "",
                "isError": "0",
                "timeStamp": "1523530744",
                "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
                "traceId": "0",
                "type": "call",
                "value": "1000000000000000000"
            },
            {
                "blockNumber": "6896101",
                "contractAddress": "",
                "errCode": "",
                "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
                "gas": "2300",
                "gasUsed": "0",
                "hash": "0xadded643661b566661969bb05dc3aa25eaa3ad6eef371d01e3af3e9386c266a9",
                "input": "",
                "isError": "0",
                "timeStamp": "1523951692",
                "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
                "traceId": "0",
                "type": "call",
                "value": "1000000000000000000"
            }
        ],
        "status": "1"
    }
    return etherscan_api_mock
