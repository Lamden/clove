from unittest.mock import patch

from clove.network import Litecoin


@patch('clove.block_explorer.cryptoid.clove_req_json')
def test_latest_block(request_mock):
    request_mock.return_value = 7312974
    assert Litecoin().latest_block == 7312974


@patch('clove.block_explorer.cryptoid.clove_req_json')
def test_get_transaction(request_mock):
    transasction_details = {
        "hash": "40875e3889aac718594b7f9d166ca4b0c8d3fb41b25f6649429643874e8aa384",
        "block": 1466656,
        "index": 136,
        "timestamp": 1533136217,
        "confirmations": 25071,
        "fees": 0.00067565,
        "total_input": 0.00494362,
        "inputs": [
            {
                "addr": "LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq",
                "amount": 0.00284974,
                "received_from": {
                    "tx": "565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50",
                    "n": 1
                }
            },
            {
                "addr": "LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq",
                "amount": 0.00209388,
                "received_from": {
                    "tx": "960e43acd9aae9a955ab51642da0b7d4e1243ab642a1a2decf06a3e3cd635194",
                    "n": 539
                }
            }
        ],
        "total_output": 0.00426797,
        "outputs": [
            {
                "addr": "MBtkgn1gWmm4FxAwp1WaXRtRZTfNLKTZzn",
                "amount": 0.00314,
                "script": "76a9142bccd91f6a56b55cca796ef7f0aaaa33c97b25a888ac"
            },
            {
                "addr": "LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq",
                "amount": 0.00112797,
                "script": "76a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac"
            }
        ]
    }
    request_mock.return_value = transasction_details
    tx = Litecoin().get_transaction('40875e3889aac718594b7f9d166ca4b0c8d3fb41b25f6649429643874e8aa384')
    assert tx == transasction_details


@patch('clove.block_explorer.cryptoid.clove_req_json')
def test_get_utxo(request_mock, fake_cryptoid_token):
    request_mock.return_value = {
        "unspent_outputs": [
            {
                "tx_hash": "c3f6835036dbf88152821927b76069e390a8876ecb7b509cf24702468736f89a",
                "tx_ouput_n": 1,
                "value": "93209",
                "confirmations": 101957,
                "script": "76a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac"
            },
            {
                "tx_hash": "393e358df3edaea4bcbfeecd58d897b03d2d472cbb48c345259d8c6afce6e62a",
                "tx_ouput_n": 0,
                "value": "57835",
                "confirmations": 94791,
                "script": "76a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac"
            },
        ]
    }

    utxo = Litecoin().get_utxo(address='LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq', amount=0.0009)
    assert len(utxo) == 1
    assert utxo[0].tx_id == 'c3f6835036dbf88152821927b76069e390a8876ecb7b509cf24702468736f89a'
    assert utxo[0].vout == 1
    assert utxo[0].value == 0.00093209
    assert utxo[0].tx_script == '76a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac'
    assert utxo[0].wallet is None
    assert utxo[0].secret is None
    assert utxo[0].refund is False

    utxo = Litecoin().get_utxo(address='LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq', amount=0.001)
    assert len(utxo) == 2


@patch('clove.block_explorer.cryptoid.clove_req_json')
def test_extract_secret_from_redeem_transaction(request_mock, fake_cryptoid_token):
    wallet_deails = {
        "addresses": [
            {
                "address": "MWXzG4RaH4VH6hiNKakxkZQqW7NSHYRGrA",
                "total_sent": 1000000,
                "total_received": 1000000,
                "final_balance": 0,
                "n_tx": 2
            }
        ],
        "txs": [
            {
                "hash": "0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec",
                "confirmations": 84777,
                "change": -1000000,
                "time_utc": "2018-04-20T11:53:50Z"
            },
            {
                "hash": "565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50",
                "confirmations": 84781,
                "change": 1000000,
                "time_utc": "2018-04-20T11:43:28Z",
                "n": 0
            }
        ]
    }
    tx_details = {
        "txid": "0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec",
        "hash": "0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec",
        "size": 343,
        "vsize": 343,
        "version": 1,
        "locktime": 0,
        "vin": [
            {
                "txid": "565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50",
                "vout": 0,
                "scriptSig": {
                    "asm": "3045022100d63353332b762551f3278ea02ab25746ddc78aae08c73cfd81e7871b54ebee88022068fa0e3b6578efbfed07373b2147b190ebe6466d2cdbed15cc2eecb0f2188370[ALL] 0459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4 9a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2 1 63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac",  # noqa: E501
                    "hex": "483045022100d63353332b762551f3278ea02ab25746ddc78aae08c73cfd81e7871b54ebee88022068fa0e3b6578efbfed07373b2147b190ebe6466d2cdbed15cc2eecb0f218837001410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4209a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac"  # noqa: E501
                },
                "sequence": 0
            }
        ],
        "vout": [
            {
                "value": 0.00976168,
                "n": 0,
                "scriptPubKey": {
                    "asm": "OP_DUP OP_HASH160 85c0522f6e23beb11cc3d066cd20ed732648a4e6 OP_EQUALVERIFY OP_CHECKSIG",
                    "hex": "76a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac",
                    "reqSigs": 1,
                    "type": "pubkeyhash",
                    "addresses": [
                        "LXRAXRgPo84p58746zaBXUFFevCTYBPxgb"
                    ]
                }
            }
        ],
        "blockhash": "596b7d88d0ff23057db0bfd2fbb071e93a0aeafa287733a7e6c957509ce1dd8b",
        "confirmations": 84779,
        "time": 1524225230,
        "blocktime": 1524225230
    }

    request_mock.side_effect = (wallet_deails, tx_details)
    secret = Litecoin().extract_secret_from_redeem_transaction('MWXzG4RaH4VH6hiNKakxkZQqW7NSHYRGrA')
    assert secret == '9a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2'


@patch('clove.block_explorer.cryptoid.clove_req_json')
def test_get_balance(request_mock, fake_cryptoid_token):
    request_mock.return_value = 0.00987407
    balance = Litecoin().get_balance('LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq')
    assert balance == 0.00987407


def test_get_transaction_url():
    url = Litecoin().get_transaction_url('123')
    assert url == 'https://chainz.cryptoid.info/ltc/tx.dws?123.htm'
