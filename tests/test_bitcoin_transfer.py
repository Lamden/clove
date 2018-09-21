from datetime import datetime, timedelta
from unittest.mock import patch

from bitcoin.core import CTransaction, b2x, script
from freezegun import freeze_time
import pytest
from pytest import raises

from clove.constants import SIGNATURE_SIZE
from clove.network import BitcoinTestNet, EthereumTestnet, Monacoin
from clove.network.bitcoin.transaction import BitcoinAtomicSwapTransaction, BitcoinTransaction
from clove.utils.bitcoin import to_base_units


def test_swap_contract(alice_wallet, bob_wallet):
    transaction = BitcoinAtomicSwapTransaction(
        BitcoinTestNet(),
        alice_wallet.address,
        bob_wallet.address,
        0.5,
        solvable_utxo=[]
    )
    transaction.set_locktime(number_of_hours=48)
    transaction.generate_hash()
    transaction.build_atomic_swap_contract()
    assert transaction.contract.is_valid()


def test_transaction_signing(unsigned_transaction):
    transaction = unsigned_transaction
    first_script_signature = transaction.tx.vin[0].scriptSig
    transaction.sign()
    second_first_script_signature = transaction.tx.vin[0].scriptSig
    assert first_script_signature != second_first_script_signature


def test_transaction_signing_with_default_wallet(alice_wallet, unsigned_transaction):
    transaction = unsigned_transaction
    unsigned_transaction.solvable_utxo[0].wallet = None
    with raises(
        RuntimeError,
        match="Cannot sign transaction without a wallet."
    ):
        transaction.sign()

    first_script_signature = transaction.tx.vin[0].scriptSig
    transaction.sign(alice_wallet)
    second_first_script_signature = transaction.tx.vin[0].scriptSig
    assert first_script_signature != second_first_script_signature


def test_show_details(signed_transaction):
    details = signed_transaction.show_details()

    assert type(details) is dict

    str_fields = (
        'contract',
        'contract_address',
        'contract_transaction',
        'transaction_address',
        'transaction_link',
        'recipient_address',
        'refund_address',
        'secret',
        'secret_hash',
        'size_text',
        'value_text',
        'fee_text',
        'fee_per_kb_text',
    )

    date_fields = (
        'locktime',
    )

    int_fields = (
        'size',
    )

    float_fields = (
        'value',
        'fee',
        'fee_per_kb',
    )

    for field in str_fields:
        assert type(details[field]) is str, 'not a string'
        assert len(details[field]), 'empty string'

    for field in date_fields:
        assert type(details[field]) is datetime, 'not a datetime'

    for field in float_fields:
        assert type(details[field]) is float, 'not a float'

    assert details['value'] == signed_transaction.value
    assert details['value_text'] == '0.70000000 BTC'

    assert details['fee_per_kb_text'].endswith('/ 1 kB')
    assert details['size_text'].endswith('bytes')

    assert sorted(details.keys()) == sorted(str_fields + date_fields + int_fields + float_fields)


def test_transaction_fee(unsigned_transaction):

    assert type(unsigned_transaction.size) == int

    unsigned_transaction.fee_per_kb = 0.002
    unsigned_transaction.add_fee()
    assert type(unsigned_transaction.fee) == float
    assert unsigned_transaction.fee < 1, 'Transaction fee should be in main units'

    change_without_fee = unsigned_transaction.tx.vout[1].nValue
    unsigned_transaction.add_fee()
    change_with_fee = unsigned_transaction.tx.vout[1].nValue

    assert change_without_fee - to_base_units(unsigned_transaction.fee) == change_with_fee
    assert unsigned_transaction.tx.serialize()


def test_calculate_fee_with_signature_size(unsigned_transaction):

    fee_per_kb = 0.002
    unsigned_transaction.fee_per_kb = fee_per_kb
    unsigned_transaction.calculate_fee(add_sig_size=True)
    size_after_sign = unsigned_transaction.size + (SIGNATURE_SIZE * len(unsigned_transaction.tx_in_list))
    assert unsigned_transaction.fee == round(size_after_sign/1000 * fee_per_kb, 8)


def test_transaction_with_invalid_recipient_address():
    with raises(ValueError, match='Given recipient address is invalid.'):
        BitcoinTransaction(BitcoinTestNet(), 'invalid_address', 0.01, [])


def test_swap_transaction_with_invalid_recipient_address(bob_wallet):
    with raises(ValueError, match='Given recipient address is invalid.'):
        BitcoinAtomicSwapTransaction(BitcoinTestNet(), bob_wallet.address, 'invalid_address', 0.01, [])


def test_swap_transaction_with_invalid_sender_address(bob_wallet):
    with raises(ValueError, match='Given sender address is invalid.'):
        BitcoinAtomicSwapTransaction(BitcoinTestNet(), 'invalid_address', bob_wallet.address, 0.01, [])


def test_swap_transaction_with_invalid_recipient_and_sender_addresses():
    with raises(ValueError, match='Given recipient and sender addresses are invalid.'):
        BitcoinAtomicSwapTransaction(BitcoinTestNet(), 'invalid_address', 'address_123', 0.01, [])


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_audit_contract(_, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    contract_details = contract.show_details()

    assert contract.locktime == signed_transaction.locktime.replace(microsecond=0)

    contract_details.pop('locktime')
    contract_details.pop('confirmations')

    for field in contract_details.keys():
        assert contract_details[field] == transaction_details[field]


def test_audit_contract_empty_transaction():
    btc_network = BitcoinTestNet()
    tx = b2x(CTransaction().serialize())

    with raises(
        ValueError, match='Given transaction has no outputs.'
    ):
        btc_network.audit_contract('', tx)


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_audit_contract_invalid_transaction(_, signed_transaction):
    btc_network = BitcoinTestNet()
    signed_transaction.tx.vout.pop(0)
    transaction_details = signed_transaction.show_details()

    with raises(
        ValueError, match='Given transaction is not a valid contract.'
    ):
        btc_network.audit_contract(transaction_details['contract'], transaction_details['contract_transaction'])


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_audit_contract_non_matching_contract(_, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = script.CScript([script.OP_TRUE]).hex()

    with raises(
        ValueError, match='Given transaction is not a valid contract.'
    ):
        btc_network.audit_contract(contract, transaction_details['contract_transaction'])


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_transaction')
@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_audit_contract_by_address_blockcypher(get_balance_mock, get_transaction_mock):
    get_transaction_mock.return_value = {
        "block_hash": "00000000d658734e67ec1b46c5f0879b1c513a8677af5780d49f0c7158bc4c92",
        "block_height": 1292546,
        "block_index": 19,
        "hash": "ed42a44cd4d45d6829fed3faa06e9dc60de3a6314fd42a80229ea85e1b4680ef",
        "hex": "0100000001bad8594e6fd26e78151d4c0b36329a0e40d6f219fb07fac5308e8bcc1cf32744010000006b4830450221008f4faade6585edbdae83c6764bd22be25bd3970856ce8d45490c9fca58b291d70220356607cae5ee31fc3d67f8484e8bb30491381af3dcb5ea2e33edfdc61a64f661012103142762372a0f6f2b4718cdee32fa1a3cc2465d3379312e8875ee5f9193158177000000000240420f000000000017a9141fe32017a8f8ad24f791dfd3128f18d0145a66fa87a0c9f003000000001976a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac00000000",  # noqa: E501
        "addresses": [
            "2Mv9q2BF9ua62vZcWQqtGdaaAki37SHVoXm",
            "msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM"
        ],
        "total": 67111904,
        "fees": 39182,
        "size": 224,
        "preference": "high",
        "relayed_by": "46.4.95.69:18333",
        "confirmed": "2018-04-12T13:47:09Z",
        "received": "2018-04-12T13:31:14.365Z",
        "ver": 1,
        "double_spend": False,
        "vin_sz": 1,
        "vout_sz": 2,
        "opt_in_rbf": True,
        "confirmations": 120829,
        "confidence": 1,
        "inputs": [
            {
                "prev_hash": "4427f31ccc8b8e30c5fa07fb19f2d6400e9a32360b4c1d15786ed26f4e59d8ba",
                "output_index": 1,
                "script": "4830450221008f4faade6585edbdae83c6764bd22be25bd3970856ce8d45490c9fca58b291d70220356607cae5ee31fc3d67f8484e8bb30491381af3dcb5ea2e33edfdc61a64f661012103142762372a0f6f2b4718cdee32fa1a3cc2465d3379312e8875ee5f9193158177",  # noqa: E501
                "output_value": 67151086,
                "sequence": 0,
                "addresses": [
                    "msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM"
                ],
                "script_type": "pay-to-pubkey-hash",
                "age": 1292283
            }
        ],
        "outputs": [
            {
                "value": 1000000,
                "script": "a9141fe32017a8f8ad24f791dfd3128f18d0145a66fa87",
                "addresses": [
                    "2Mv9q2BF9ua62vZcWQqtGdaaAki37SHVoXm"
                ],
                "script_type": "pay-to-script-hash"
            },
            {
                "value": 66111904,
                "script": "76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac",
                "spent_by": "2bd59cfdd58af477756bd3bde263e2d875e741d7aa828bc8af398960083dbfbe",
                "addresses": [
                    "msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM"
                ],
                "script_type": "pay-to-pubkey-hash"
            }
        ]
    }
    btc_network = BitcoinTestNet()
    contract = btc_network.audit_contract(
        contract=(
            '63a614977afed2fcdfea9d27fd3032b4a1bc20219007f18876a9143f8870a5633e4fdac612fba4752'
            '5fef082bbe96167049b02d25ab17576a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b6888ac'
        ),
        transaction_address='ed42a44cd4d45d6829fed3faa06e9dc60de3a6314fd42a80229ea85e1b4680ef'
    )
    details = contract.show_details()

    confirmations = details.pop('confirmations')
    assert type(confirmations) is int
    assert confirmations > 0

    assert details == {
        'contract_address': '2Mv9q2BF9ua62vZcWQqtGdaaAki37SHVoXm',
        'locktime': datetime(2018, 4, 14, 13, 31, 7),
        'recipient_address': 'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1',
        'refund_address': 'msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM',
        'secret_hash': '977afed2fcdfea9d27fd3032b4a1bc20219007f1',
        'transaction_address': 'ed42a44cd4d45d6829fed3faa06e9dc60de3a6314fd42a80229ea85e1b4680ef',
        'transaction_link': (
            'https://live.blockcypher.com/btc-testnet/tx/'
            'ed42a44cd4d45d6829fed3faa06e9dc60de3a6314fd42a80229ea85e1b4680ef/'
        ),
        'value': 0.01,
        'value_text': '0.01000000 BTC'
    }


@patch('clove.block_explorer.insight.InsightAPIv4.get_transaction')
@patch('clove.block_explorer.insight.InsightAPIv4.get_balance', return_value=0.01)
def test_audit_contract_by_address_insight(get_balance_mock, get_transaction_mock):
    get_transaction_mock.return_value = {
        'txid': '693b04a205a8b87942bff07f8855f00e7a4378b839c8a264dfc849e8331ba6d4',
        'version': 1,
        'locktime': 0,
        'vin': [{
            'txid': '61042a641baf7db7b15fb80bac5c85b5346fc8a383b9b634baf006fb7b762997',
            'vout': 0,
            'sequence': 0,
            'n': 0,
            'scriptSig': {
                'hex': '483045022100ddfb15614affeeee2fc7667956d7d51237640dc0c29a3b1adfb8b9fc1a2a352f02206147ccdfda804d751f4df9282b5d7d0bdc1b2f9d6180332251566040a98d445501210240917aa65f12d8051abae7e8e98eea3b085a766a2dd7bd7f71c8121304cca298',  # noqa: E501
                'asm': '3045022100ddfb15614affeeee2fc7667956d7d51237640dc0c29a3b1adfb8b9fc1a2a352f02206147ccdfda804d751f4df9282b5d7d0bdc1b2f9d6180332251566040a98d4455[ALL] 0240917aa65f12d8051abae7e8e98eea3b085a766a2dd7bd7f71c8121304cca298'   # noqa: E501
            },
            'addr': 'MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP',
            'valueSat': 22234100,
            'value': 0.222341,
            'doubleSpentTxID': None
         }],
        'vout': [
            {
                'value': '0.01000000',
                'n': 0,
                'scriptPubKey': {
                    'hex': 'a914d8fadb4bb1b13492e966f02b2fc482e81bb62ea787',
                    'asm': 'OP_HASH160 d8fadb4bb1b13492e966f02b2fc482e81bb62ea7 OP_EQUAL',
                    'addresses': ['PUNTdERe8wX5Pnb42siEshZ41VY2zpzJXj'],
                    'type': 'scripthash'
                },
                'spentTxId': None,
                'spentIndex': None,
                'spentHeight': None
            },
            {
                'value': '0.21129707',
                'n': 1,
                'scriptPubKey': {
                    'hex': '76a914a96a92963b7a65ac904875cfa5d535b31158882788ac',
                    'asm': 'OP_DUP OP_HASH160 a96a92963b7a65ac904875cfa5d535b311588827 OP_EQUALVERIFY OP_CHECKSIG',
                    'addresses': ['MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP'],
                    'type': 'pubkeyhash'
                },
                'spentTxId': None,
                'spentIndex': None,
                'spentHeight': None
            }
        ],
        'blockhash': '4f31e74f6c1187b7bdeb6887a5b334ba8875539b511cd67f07ab57c00a2e3df4',
        'blockheight': 1445790,
        'confirmations': 50,
        'time': 1537543050,
        'blocktime': 1537543050,
        'valueOut': 0.22129707,
        'size': 224,
        'valueIn': 0.222341,
        'fees': 0.00104393
    }

    mona_network = Monacoin()
    contract = mona_network.audit_contract(
        contract=(
            '63a6141c1a607a3ab21817158df2902c928baf43a9da438876a914fbed00c1502fded3dfa2524f8672'
            'ee013bb3f28f6704c9aba75bb17576a914a96a92963b7a65ac904875cfa5d535b3115888276888ac'
        ),
        transaction_address='693b04a205a8b87942bff07f8855f00e7a4378b839c8a264dfc849e8331ba6d4'
    )
    details = contract.show_details()

    confirmations = details.pop('confirmations')
    assert type(confirmations) is int
    assert confirmations > 0

    assert details == {
        'contract_address': 'PUNTdERe8wX5Pnb42siEshZ41VY2zpzJXj',
        'transaction_address': '693b04a205a8b87942bff07f8855f00e7a4378b839c8a264dfc849e8331ba6d4',
        'transaction_link':
            'https://insight.electrum-mona.org/'
            'insight/tx/693b04a205a8b87942bff07f8855f00e7a4378b839c8a264dfc849e8331ba6d4',
        'locktime': datetime(2018, 9, 23, 15, 5, 45),
        'recipient_address': 'MWsDkqHLonS5KfbRnRu3feByD9qkuj44Ye',
        'refund_address': 'MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP',
        'secret_hash': '1c1a607a3ab21817158df2902c928baf43a9da43',
        'value': 0.01,
        'value_text': '0.01000000 MONA'
    }


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_redeem_transaction(_, bob_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    redeem_transaction = contract.redeem(bob_wallet, transaction_details['secret'])
    redeem_transaction.fee_per_kb = 0.002
    redeem_transaction.add_fee_and_sign()

    assert redeem_transaction.recipient_address == bob_wallet.address
    assert redeem_transaction.value == signed_transaction.value


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.0)
def test_redeem_transaction_zero_balance(_, btc_testnet_contract, bob_wallet):
    with pytest.raises(ValueError) as e:
        btc_testnet_contract.redeem(bob_wallet, 'such_secret')
    assert str(e.value) == 'Balance of this contract is 0.'


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_refund_transaction(_, alice_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )

    with freeze_time(transaction_details['locktime']):
        refund_transaction = contract.refund(alice_wallet)

    refund_transaction.fee_per_kb = 0.002
    refund_transaction.add_fee_and_sign()

    assert refund_transaction.recipient_address == alice_wallet.address
    assert refund_transaction.value == signed_transaction.value


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_refund_not_expired_contract(_, alice_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )

    with freeze_time(transaction_details['locktime'] - timedelta(seconds=1)):
        locktime_string = transaction_details['locktime'].strftime('%Y-%m-%d %H:%M:%S')
        with raises(
            RuntimeError, match=f"This contract is still valid! It can't be refunded until {locktime_string}."
        ):
            contract.refund(alice_wallet)


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.0)
def test_refund_zero_balance(_, btc_testnet_contract, bob_wallet):
    with freeze_time(btc_testnet_contract.locktime + timedelta(days=5)):
        with pytest.raises(ValueError) as e:
            btc_testnet_contract.refund(bob_wallet)
    assert str(e.value) == 'Balance of this contract is 0.'


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_participate_transaction(_, alice_wallet, bob_wallet, bob_utxo, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    participate_value = 0.5
    participate_transaction = contract.participate(
        'BTC-TESTNET', bob_wallet.address, alice_wallet.address, participate_value, bob_utxo
    )
    participate_transaction.fee_per_kb = 0.002
    participate_transaction.add_fee_and_sign()

    assert participate_transaction.sender_address == bob_wallet.address
    assert participate_transaction.recipient_address == alice_wallet.address
    assert participate_transaction.value == participate_value
    assert participate_transaction.secret_hash == signed_transaction.secret_hash
    assert participate_transaction.secret is None
    assert isinstance(participate_transaction.network, BitcoinTestNet)

    participate_transaction_details = participate_transaction.show_details()

    contract = btc_network.audit_contract(
        participate_transaction_details['contract'],
        participate_transaction_details['contract_transaction']
    )
    redeem_participate_transaction = contract.redeem(alice_wallet, transaction_details['secret'])
    redeem_participate_transaction.fee_per_kb = 0.002
    redeem_participate_transaction.add_fee_and_sign()

    assert redeem_participate_transaction.recipient_address == alice_wallet.address
    assert redeem_participate_transaction.value == participate_value


def test_participate_eth_transaction(signed_transaction, infura_token):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    alice_eth_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    bob_eth_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    participate_value = 0.5
    participate_transaction = contract.participate(
        'ETH-TESTNET', alice_eth_address, bob_eth_address, participate_value
    )

    assert participate_transaction.sender_address == alice_eth_address
    assert participate_transaction.recipient_address == bob_eth_address
    assert participate_transaction.value == participate_value
    assert participate_transaction.secret_hash == signed_transaction.secret_hash
    assert participate_transaction.secret is None
    assert isinstance(participate_transaction.network, EthereumTestnet)


@patch('clove.block_explorer.blockcypher.BlockcypherAPI.get_balance', return_value=0.01)
def test_extract_secret(_, bob_wallet, signed_transaction):
    btc_network = BitcoinTestNet()
    transaction_details = signed_transaction.show_details()

    contract = btc_network.audit_contract(
        transaction_details['contract'],
        transaction_details['contract_transaction']
    )
    redeem_transaction = contract.redeem(bob_wallet, transaction_details['secret'])
    redeem_transaction.fee_per_kb = 0.002
    redeem_transaction.add_fee_and_sign()

    redeem_details = redeem_transaction.show_details()

    secret = btc_network.extract_secret(redeem_details['transaction'])

    assert secret == transaction_details['secret']

    # extracting secret from scriptSig
    assert secret == btc_network.extract_secret(scriptsig=redeem_transaction.tx.vin[0].scriptSig.hex())


def test_transaction_link_in_unsigned_transaction(unsigned_transaction):

    assert 'transaction_link' not in unsigned_transaction.show_details()


def test_transaction_link_in_signed_transaction(signed_transaction):

    assert signed_transaction.show_details()['transaction_link'].startswith('http')
