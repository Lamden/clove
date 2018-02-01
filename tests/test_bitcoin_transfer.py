from clove.network.bitcoin import BitcoinTransaction, TestNetBitcoin


def test_swap_contract(alice_wallet, bob_wallet):
    transaction = BitcoinTransaction(
        TestNetBitcoin(),
        alice_wallet.get_address(),
        bob_wallet.get_address(),
        0.5,
        outpoints={}
    )
    transaction.set_locktime(number_of_hours=48)
    transaction.generate_hash()
    transaction.build_atomic_swap_contract()
    assert transaction.contract.is_valid()


def test_initiate_atomic_swap(alice_wallet, bob_wallet):
    btc_network = TestNetBitcoin()
    outpoints = [
        {
            'txid': '6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8',
            'vout': 1,
            'value': 0.78956946,
            'scriptPubKey': '76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac'
        },
    ]
    transaction = btc_network.initiate_atomic_swap(
        alice_wallet.get_address(),
        bob_wallet.get_address(),
        0.00001,
        outpoints
    )
    first_script_signature = transaction.tx.vin[0].scriptSig
    transaction.sign(alice_wallet)
    second_first_script_signature = transaction.tx.vin[0].scriptSig
    assert first_script_signature != second_first_script_signature
