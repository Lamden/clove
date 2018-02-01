from collections import namedtuple

import pytest

from clove.network.bitcoin import BitcoinWallet

Key = namedtuple('Key', ['secret', 'address'])


@pytest.fixture
def alice_wallet():
    return BitcoinWallet(private_key='cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe', testnet=True)


@pytest.fixture
def bob_wallet():
    return BitcoinWallet(private_key='cRoFBWMvcLXrLsYFt794NRBEPUgMLf5AmnJ7VQwiEenc34z7zSpK', testnet=True)
