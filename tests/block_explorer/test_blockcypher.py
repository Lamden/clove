from unittest.mock import patch

from clove.network import BitcoinTestNet


@patch('clove.block_explorer.blockcypher.clove_req_json')
def test_latest_block(request_mock):
    request_mock.return_value = {
        "name": "BTC.test3",
        "height": 1413369,
        "hash": "00000000498be6e8c38597d9825bb210846afe3a68578eb66cd8682f76315c3d",
        "time": "2018-09-13T15:23:51.040868425Z",
        "latest_url": "https://api.blockcypher.com/v1/btc/test3/blocks/00000000498be6e8c38597d9825bb210846afe3a68578eb66cd8682f76315c3d",  # noqa: E501
        "previous_hash": "00000000801ddbbd27d6d2b997ba79aaeefb85c869b2798d48984748cf5fbc0f",
        "previous_url": "https://api.blockcypher.com/v1/btc/test3/blocks/00000000801ddbbd27d6d2b997ba79aaeefb85c869b2798d48984748cf5fbc0f",  # noqa: E501
        "peer_count": 285,
        "unconfirmed_count": 16599,
        "high_fee_per_kb": 7988228,
        "medium_fee_per_kb": 10000,
        "low_fee_per_kb": 7000,
        "last_fork_height": 1412892,
        "last_fork_hash": "00000000e7db755cf751a8811cc612b07bf2b519180cca85e25c45db5ce77a3e"
    }
    assert BitcoinTestNet().latest_block == 1413369


@patch('clove.block_explorer.blockcypher.clove_req_json')
def test_get_transaction(request_mock):
    BitcoinTestNet().get_transaction('123')
    assert 'includeHex=true' in request_mock.call_args[0][0]


@patch('clove.block_explorer.blockcypher.clove_req_json')
def test_get_utxo(request_mock):
    request_mock.return_value = {
        "address": "msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM",
        "total_received": 846232274,
        "total_sent": 419093729,
        "balance": 427138545,
        "unconfirmed_balance": 0,
        "final_balance": 427138545,
        "n_tx": 214,
        "unconfirmed_n_tx": 0,
        "final_n_tx": 214,
        "txrefs": [
            {
                "tx_hash": "b8a5453a038f11080a346f63f5c0154dfef8a1b4d36ec6f587066ef2e86f1e30",
                "block_height": 1412850,
                "tx_input_n": -1,
                "tx_output_n": 1,
                "value": 99497174,
                "ref_balance": 527646969,
                "spent": False,
                "confirmations": 521,
                "confirmed": "2018-09-10T13:04:59Z",
                "double_spend": False,
                "script": "76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac"
            }, {
                "tx_hash": "d54c26089d1d499f9218153795ff4246ede6f2121c9584b142bbed7917871f5a",
                "block_height": 1410198,
                "tx_input_n": -1,
                "tx_output_n": 0,
                "value": 510469,
                "ref_balance": 428149795,
                "spent": False,
                "confirmations": 3173,
                "confirmed": "2018-08-27T16:32:33Z",
                "double_spend": False,
                "script": "76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac"
            }
        ],
        "hasMore": True,
        "tx_url": "https://api.blockcypher.com/v1/btc/test3/txs/"
    }

    utxo = BitcoinTestNet().get_utxo(address='msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM', amount=0.9)
    assert len(utxo) == 1
    assert utxo[0].tx_id == 'b8a5453a038f11080a346f63f5c0154dfef8a1b4d36ec6f587066ef2e86f1e30'
    assert utxo[0].vout == 1
    assert utxo[0].value == 0.99497174
    assert utxo[0].tx_script == '76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac'
    assert utxo[0].wallet is None
    assert utxo[0].secret is None
    assert utxo[0].refund is False

    utxo = BitcoinTestNet().get_utxo(address='msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM', amount=0.996)
    assert len(utxo) == 2


@patch('clove.block_explorer.blockcypher.clove_req_json')
def test_extract_secret_from_redeem_transaction(request_mock):
    request_mock.return_value = {
        "address": "2N7Gxryn4dD1mdyGM3DMxMAwD7k3RBTJ1gP",
        "total_received": 1000000,
        "total_sent": 1000000,
        "balance": 0,
        "unconfirmed_balance": 0,
        "final_balance": 0,
        "n_tx": 2,
        "unconfirmed_n_tx": 0,
        "final_n_tx": 2,
        "txs": [
            {
                "block_hash": "00000000000000bf4419ccb594857545356f9ab7b4c22be0dc1496a2b3cfc3fb",
                "block_height": 1410198,
                "block_index": 627,
                "hash": "d54c26089d1d499f9218153795ff4246ede6f2121c9584b142bbed7917871f5a",
                "addresses": [
                    "2N7Gxryn4dD1mdyGM3DMxMAwD7k3RBTJ1gP",
                    "msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM"
                ],
                "total": 510469,
                "fees": 489531,
                "size": 308,
                "preference": "high",
                "relayed_by": "52.52.49.111:18333",
                "confirmed": "2018-08-27T16:32:33Z",
                "received": "2018-08-27T16:27:45.847Z",
                "ver": 1,
                "double_spend": False,
                "vin_sz": 1,
                "vout_sz": 1,
                "opt_in_rbf": True,
                "confirmations": 3177,
                "confidence": 1,
                "inputs": [
                    {
                        "prev_hash": "47e1cf28e6ddb6c38018fc3a80e69c8474bd657575cd2c2f1cb8ea45f7126f07",
                        "output_index": 0,
                        "script": "473044022045720f2caebbe0f6bbc3478548657ddbbb4242f3ce715f96a219dfaf9bcb80ef02204897b23e1040dd540aefc3fbc0aaa67af64923870848e140398c98490a73f449012103142762372a0f6f2b4718cdee32fa1a3cc2465d3379312e8875ee5f91931581772090f6b9b9a34acb486654b3e9cdc02cce0b8e40a8845924ffda68453ac2477d20514c5163a614e4791338b198aa7af8e37d14f2bd76991da4efc48876a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b6704e074855bb17576a9143f8870a5633e4fdac612fba47525fef082bbe9616888ac",  # noqa: E501
                        "output_value": 1000000,
                        "sequence": 0,
                        "addresses": [
                            "2N7Gxryn4dD1mdyGM3DMxMAwD7k3RBTJ1gP"
                        ],
                        "script_type": "pay-to-script-hash",
                        "age": 1410195
                    }
                ],
                "outputs": [
                    {
                        "value": 510469,
                        "script": "76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac",
                        "addresses": [
                            "msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM"
                        ],
                        "script_type": "pay-to-pubkey-hash"
                    }
                ]
            },
            {
                "block_hash": "00000000000000caaf80ebfd9ef9e61ffffad9f5aaa044bd77f945e6814a57d7",
                "block_height": 1410195,
                "block_index": 1081,
                "hash": "47e1cf28e6ddb6c38018fc3a80e69c8474bd657575cd2c2f1cb8ea45f7126f07",
                "addresses": [
                    "2N7Gxryn4dD1mdyGM3DMxMAwD7k3RBTJ1gP",
                    "mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1"
                ],
                "total": 183249749,
                "fees": 359982,
                "size": 223,
                "preference": "high",
                "relayed_by": "37.59.44.40:18333",
                "confirmed": "2018-08-27T16:19:44Z",
                "received": "2018-08-27T16:18:38.317Z",
                "ver": 1,
                "double_spend": False,
                "vin_sz": 1,
                "vout_sz": 2,
                "opt_in_rbf": True,
                "confirmations": 3180,
                "confidence": 1,
                "inputs": [
                    {
                        "prev_hash": "2e362c56325d8c5baf438707ae438d96797f90b6e4f5458bf96a033505c412eb",
                        "output_index": 1,
                        "script": "47304402201354e12202bb4a40274ff05d48960c9284dbdf2d2d709f779ff4d55cbe932bac022053637603aab90648de3b97563b483d65aaa5142e596ce07e2c42b97df2b65ce1012102187b57bba6e143aca9da3557fe8bcf912379ca7ffb8c1967ca6dbde2dc695f19",  # noqa: E501
                        "output_value": 183609731,
                        "sequence": 0,
                        "addresses": [
                            "mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1"
                        ],
                        "script_type": "pay-to-pubkey-hash",
                        "age": 1410149
                    }
                ],
                "outputs": [
                    {
                        "value": 1000000,
                        "script": "a91499e5f7661d571c39d3cf415a52bde28f208ebada87",
                        "spent_by": "d54c26089d1d499f9218153795ff4246ede6f2121c9584b142bbed7917871f5a",
                        "addresses": [
                            "2N7Gxryn4dD1mdyGM3DMxMAwD7k3RBTJ1gP"
                        ],
                        "script_type": "pay-to-script-hash"
                    },
                    {
                        "value": 182249749,
                        "script": "76a9143f8870a5633e4fdac612fba47525fef082bbe96188ac",
                        "spent_by": "f754a630ede341f30094bc165602b235e2b26a2168e8eddffd7987bb0b504e42",
                        "addresses": [
                            "mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1"
                        ],
                        "script_type": "pay-to-pubkey-hash"
                    }
                ]
            }
        ]
    }
    secret = BitcoinTestNet().extract_secret_from_redeem_transaction('2N7Gxryn4dD1mdyGM3DMxMAwD7k3RBTJ1gP')
    assert secret == '90f6b9b9a34acb486654b3e9cdc02cce0b8e40a8845924ffda68453ac2477d20'


@patch('clove.block_explorer.blockcypher.clove_req_json')
def test_get_balance(request_mock):
    request_mock.return_value = {
        "address": "msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM",
        "total_received": 846232274,
        "total_sent": 419093729,
        "balance": 427138545,
        "unconfirmed_balance": 0,
        "final_balance": 427138545,
        "n_tx": 214,
        "unconfirmed_n_tx": 0,
        "final_n_tx": 214
    }
    balance = BitcoinTestNet().get_balance('msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM')
    assert balance == 4.27138545


def test_get_transaction_url():
    url = BitcoinTestNet().get_transaction_url('123')
    assert url == 'https://live.blockcypher.com/btc-testnet/tx/123/'
