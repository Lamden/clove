from unittest.mock import patch

from clove.network import Monacoin
from clove.network.bitcoin.utxo import Utxo


@patch('clove.block_explorer.monacoin.clove_req_json')
def test_latest_block(request_mock):
    request_mock.return_value = {"blocks": 1439145}
    assert Monacoin().latest_block == 1439145


@patch('clove.block_explorer.monacoin.clove_req_json')
def test_getting_utxo(request_mock):
    request_mock.return_value = [
        {
            "txid": "e0832ca854e4577cab20413013d6251c4a426022112d9ff222067bb5d8b6b723",
            "vout": 0,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 098671104a3dd5b8eb1559929221d946073a34ba OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac",
                "type": "pubkeyhash",
                "address": "M8mXNKtwFoW765V8VEbhZ8TNCqywFr25in"
            },
            "value": 90000070
        },
        {
            "txid": "308b997d8583aa48a7b265246eb76e5d030495468bbb87989606aea769b03600",
            "vout": 1,
            "scriptPubKey": {
                "asm": "OP_DUP OP_HASH160 098671104a3dd5b8eb1559929221d946073a34ba OP_EQUALVERIFY OP_CHECKSIG",
                "hex": "76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac",
                "type": "pubkeyhash",
                "address": "M8mXNKtwFoW765V8VEbhZ8TNCqywFr25in"
            },
            "value": 15500105
        },
    ]
    expected_utxo = [
        Utxo(
            tx_id='e0832ca854e4577cab20413013d6251c4a426022112d9ff222067bb5d8b6b723',
            vout=0,
            value=0.9000007,
            tx_script='76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac'
        ),
        Utxo(
            tx_id='308b997d8583aa48a7b265246eb76e5d030495468bbb87989606aea769b03600',
            vout=1,
            value=0.15500105,
            tx_script='76a9143804c5840717fb1c5c8ac0bd2726556a51e91fcd99ac'
        )
    ]
    expected_utxo_dicts = [utxo.__dict__ for utxo in expected_utxo]
    network = Monacoin()
    address = 'testaddress'
    amount = 1.0
    assert [utxo.__dict__ for utxo in network.get_utxo(address, amount)] == expected_utxo_dicts
    assert request_mock.call_args[0][0].startswith('https://mona.chainseeker.info/api/v1/utxos/')


@patch('clove.block_explorer.monacoin.clove_req_json')
def test_extract_secret_monacoin(request_mock):
    contract_transactions_mock = [
        'a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4',
        '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697'
    ]
    redeem_transaction_details = {
        'confirmed_height': 1304882,
        'hash': '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697',
        'hex': (
            '0100000001e4f0bb83bc3b52f921ad9d064768ba1702d9ec92befa3529a17e5163c90a11a000000000fd0001483045022100'
            'bf0dec5ab03d024147bc26df33a64f2389c4647fc1f9a92e93575cb5f2ff5081022060a54dd5135bc38eb6e75c65ec4e47ef'
            'a08e7298fed83757db31bd53619a17d501410447408e366d0e979101f776ab10753091b0b62ba9aa609d006263959e030fb2'
            'd96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1abb209a2cfc32611dbd3ac3261cd23622223e'
            '85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57646b3e056514185a97d15a7f086e8876a9141a376f66'
            '34e41c22b28bc9ef3336a623717083a46704ef6bdc5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac'
            '000000000160d36002000000001976a9141a376f6634e41c22b28bc9ef3336a623717083a488ac00000000'
        ),
        'locktime': 0,
        'size': 343,
        'txid': '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697',
        'version': 1,
        'vin': [{
            'address': 'PXGT7u4hd6gKYuzBkNUGsufYDARVAhoYue',
            'scriptSig': {
                'asm': (
                    '3045022100bf0dec5ab03d024147bc26df33a64f2389c4647fc1f9a92e93575cb5f2ff5081022060a54dd5135bc3'
                    '8eb6e75c65ec4e47efa08e7298fed83757db31bd53619a17d501 0447408e366d0e979101f776ab10753091b0b62'
                    'ba9aa609d006263959e030fb2d96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1abb '
                    '9a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2 OP_TRUE 63a61498ff8f419c576'
                    '46b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab1757'
                    '6a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac'
                ),
                'hex': (
                    '483045022100bf0dec5ab03d024147bc26df33a64f2389c4647fc1f9a92e93575cb5f2ff5081022060a54dd5135b'
                    'c38eb6e75c65ec4e47efa08e7298fed83757db31bd53619a17d501410447408e366d0e979101f776ab10753091b0'
                    'b62ba9aa609d006263959e030fb2d96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1a'
                    'bb209a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57'
                    '646b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab175'
                    '76a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac'
                )
            },
            'sequence': 0,
            'txid': 'a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4',
            'txinwitness': [],
            'value': 40000000,
            'vout': 0
        }],
        'vout': [{
            'n': 0,
            'scriptPubKey': {
                'address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
                'asm': 'OP_DUP OP_HASH160 1a376f6634e41c22b28bc9ef3336a623717083a4 OP_EQUALVERIFY OP_CHECKSIG',
                'hex': '76a9141a376f6634e41c22b28bc9ef3336a623717083a488ac',
                'type': 'pubkeyhash'
            },
            'value': 39900000
        }],
        'vsize': 343
    }
    request_mock.side_effect = (contract_transactions_mock, redeem_transaction_details)
    monacoin = Monacoin()
    secret = monacoin.extract_secret_from_redeem_transaction(contract_address='PXGT7u4hd6gKYuzBkNUGsufYDARVAhoYue')
    assert secret == '9a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2'


def test_get_transaction_url():
    url = Monacoin().get_transaction_url('123')
    assert url == 'https://mona.chainseeker.info/tx/123'
