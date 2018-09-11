from unittest.mock import patch

from clove.network import Ravencoin


@patch('clove.block_explorer.insight.clove_req_json')
def test_latest_block(request_mock):
    request_mock.return_value = {
        "info": {
            "version": 2000400,
            "protocolversion": 70016,
            "walletversion": 10500,
            "blocks": 360681,
            "timeoffset": -1,
            "connections": 123,
            "proxy": "",
            "difficulty": 29252.44009753307,
            "testnet": False,
            "relayfee": 1e-05,
            "errors": "",
            "network": "livenet",
            "reward": 500000000000
        }
    }
    assert Ravencoin().latest_block == 360681


@patch('clove.block_explorer.insight.clove_req_json')
def test_get_transaction(request_mock):
    tx_details = {
        "txid": "8a673e9fcf5ea469e7c4180846834905e8d4c0f16c6e6ab9531efbb9112bc5e1",
        "version": 1,
        "locktime": 0,
        "vin": [
            {
                "txid": "b8ef7ddb345cfedb2b27ef75c135cae2e4db9fc40ffd023ebd0158f7eb4874e6",
                "vout": 1,
                "sequence": 0,
                "n": 0,
                "scriptSig": {
                    "hex": "483045022100862e2bd16582bfe19691676e753378f415179cfc3f74e3622f9d267f8409e2ec02207450a6e81f781dbd8ee64e33feb7c71ee5c3d650ea1a556f572f394b3addeb4f012102446c697897213c503a66aa0cd966abfcb7e92e8c65ad8dbbfbd635d15c168564",  # noqa: E501
                    "asm": "3045022100862e2bd16582bfe19691676e753378f415179cfc3f74e3622f9d267f8409e2ec02207450a6e81f781dbd8ee64e33feb7c71ee5c3d650ea1a556f572f394b3addeb4f[ALL] 02446c697897213c503a66aa0cd966abfcb7e92e8c65ad8dbbfbd635d15c168564"  # noqa: E501
                },
                "addr": "RM7w75BcC21LzxRe62jy8JhFYykRedqu8k",
                "valueSat": 1000000000,
                "value": 10,
                "doubleSpentTxID": None
            }
        ],
        "vout": [
            {
                "value": "1.00000000",
                "n": 0,
                "scriptPubKey": {
                    "hex": "a9147dd65fb484d23dfca228b591e6d9989146ff23e187",
                    "asm": "OP_HASH160 7dd65fb484d23dfca228b591e6d9989146ff23e1 OP_EQUAL",
                    "addresses": [
                        "rHhxQBbAnbSsi3QPafhgzAWQvt1iTrvTTQ"
                    ],
                    "type": "scripthash"
                },
                "spentTxId": None,
                "spentIndex": None,
                "spentHeight": None
            },
            {
                "value": "8.99000000",
                "n": 1,
                "scriptPubKey": {
                    "hex": "76a91481e1444c2585307171a36822e0dac6be8994a02588ac",
                    "asm": "OP_DUP OP_HASH160 81e1444c2585307171a36822e0dac6be8994a025 OP_EQUALVERIFY OP_CHECKSIG",
                    "addresses": [
                        "RM7w75BcC21LzxRe62jy8JhFYykRedqu8k"
                    ],
                    "type": "pubkeyhash"
                },
                "spentTxId": None,
                "spentIndex": None,
                "spentHeight": None
            }
        ],
        "blockhash": "000000000001d3d556b1b4dcdea1293ede12752f09b2d9c198d64a61b3e003ff",
        "blockheight": 108940,
        "confirmations": 251745,
        "time": 1520257531,
        "blocktime": 1520257531,
        "valueOut": 9.99,
        "size": 224,
        "valueIn": 10,
        "fees": 0.01
    }
    request_mock.return_value = tx_details
    tx = Ravencoin().get_transaction('123')
    assert tx == tx_details


@patch('clove.block_explorer.insight.clove_req_json')
def test_get_utxo(request_mock):
    request_mock.return_value = [
        {
            "address": "RM7w75BcC21LzxRe62jy8JhFYykRedqu8k",
            "txid": "8a673e9fcf5ea469e7c4180846834905e8d4c0f16c6e6ab9531efbb9112bc5e1",
            "vout": 1,
            "scriptPubKey": "76a91481e1444c2585307171a36822e0dac6be8994a02588ac",
            "amount": 8.99,
            "satoshis": 899000000,
            "height": 108940,
            "confirmations": 251750
        },
        {
            "address": "RM7w75BcC21LzxRe62jy8JhFYykRedqu8k",
            "txid": "9aad6d94d91353ff1ef6206e25364741978e8ec8ae19a6435754d6acd583e52c",
            "vout": 1,
            "scriptPubKey": "76a91481e1444c2585307171a36822e0dac6be8994a02588ac",
            "amount": 10,
            "satoshis": 1000000000,
            "height": 105935,
            "confirmations": 254755
        }
    ]

    utxo = Ravencoin().get_utxo(address='RM7w75BcC21LzxRe62jy8JhFYykRedqu8k', amount=9)
    assert len(utxo) == 1
    assert utxo[0].tx_id == '9aad6d94d91353ff1ef6206e25364741978e8ec8ae19a6435754d6acd583e52c'
    assert utxo[0].vout == 1
    assert utxo[0].value == 10
    assert utxo[0].tx_script == '76a91481e1444c2585307171a36822e0dac6be8994a02588ac'
    assert utxo[0].wallet is None
    assert utxo[0].secret is None
    assert utxo[0].refund is False

    utxo = Ravencoin().get_utxo(address='RM7w75BcC21LzxRe62jy8JhFYykRedqu8k', amount=11)
    assert len(utxo) == 2


@patch('clove.block_explorer.insight.clove_req_json')
def test_get_balance(request_mock):
    request_mock.return_value = 1899000000
    balance = Ravencoin().get_balance('RM7w75BcC21LzxRe62jy8JhFYykRedqu8k')
    assert balance == 18.99


def test_get_transaction_url():
    url = Ravencoin().get_transaction_url('123')
    assert url == 'https://ravencoin.network/tx/123'
