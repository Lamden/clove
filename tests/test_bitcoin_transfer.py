from clove.network.bitcoin import Bitcoin, BitcoinTransaction


def test_swap_contract():
    first_address = '1JvDywcLY4mKVPb2RvsjYri8qiuMNG13cr'
    second_address = '12BTnbfFRBLEwsfYVyexpUEADyNfEKwY8h'
    transaction = BitcoinTransaction(Bitcoin, first_address, second_address, 0.5, outpoints={})
    transaction.set_locktime(number_of_hours=48)
    transaction.generate_hash()
    transaction.build_atomic_swap_contract()
    assert transaction.contract.is_valid()
