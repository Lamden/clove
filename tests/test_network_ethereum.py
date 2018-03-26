import os

from clove.network import Ethereum


def test_atomic_swap():
    os.environ['INFURA_TOKEN'] = '123'
    bob_address = '0xd867f293ba129629a9f9355fa285b8d3711a9092'
    network = Ethereum()
    raw_contract = network.atomic_swap(bob_address, hours_to_expiration=48)
    assert type(raw_contract) is dict
