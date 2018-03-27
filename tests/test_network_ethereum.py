from clove.network import EthereumTestnet
from clove.network.ethereum.transaction import EthereumAtomicSwapTransaction


def test_atomic_swap(infura_token):
    alice_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    bob_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    network = EthereumTestnet()
    eth_atomic_swap = network.atomic_swap(sender_address=alice_address, recipient_address=bob_address, value=3)
    assert isinstance(eth_atomic_swap, EthereumAtomicSwapTransaction)
