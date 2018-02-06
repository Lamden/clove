from collections import namedtuple

import pytest

from clove.network.bitcoin import BitcoinTestNet

Key = namedtuple('Key', ['secret', 'address'])


@pytest.fixture
def alice_wallet():
    return BitcoinTestNet.get_wallet(private_key='cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe')


@pytest.fixture
def bob_wallet():
    return BitcoinTestNet.get_wallet(private_key='cRoFBWMvcLXrLsYFt794NRBEPUgMLf5AmnJ7VQwiEenc34z7zSpK')


@pytest.fixture
def alice_outpoints():
    return [
        {
            'txid': '6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8',
            'vout': 1,
            'value': 0.78956946,
            'script': '76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac'
        },
    ]


@pytest.fixture
def unsigned_transaction(alice_wallet, bob_wallet, alice_outpoints):
    btc_network = BitcoinTestNet()
    transaction = btc_network.initiate_atomic_swap(
        alice_wallet.get_address(),
        bob_wallet.get_address(),
        0.7,
        alice_outpoints
    )
    return transaction


@pytest.fixture
def signed_transaction(alice_wallet, unsigned_transaction):
    transaction = unsigned_transaction
    transaction.fee_per_kb = 0.002
    transaction.add_fee_and_sign(alice_wallet)
    return transaction
