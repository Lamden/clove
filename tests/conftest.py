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


@pytest.fixture
def alice_outpoints():
    return [
        {
            'txid': '6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8',
            'vout': 1,
            'value': 0.78956946,
            'scriptPubKey': '76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac'
        },
    ]
