from clove.network.ethereum.base import EthereumBaseNetwork
from clove.network.ethereum.token import EthereumTestnetToken, EthereumToken
from clove.network.ethereum_based.kovan_tokens import kovan_tokens
from clove.network.ethereum_based.mainnet_tokens import tokens


class Ethereum(EthereumBaseNetwork):

    name = 'ethereum'
    symbols = ('ETH',)
    infura_network = 'mainnet'
    tokens = tokens
    token_class = EthereumToken
    etherscan_api_subdomain = 'api'

    # downloaded from 'Contract ABI' at etherscan.io
    abi = [{
        'constant': False,
        'inputs': [{
            'name': '_hash',
            'type': 'bytes20'
        }],
        'name': 'refund',
        'outputs': [],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }, {
        'constant': False,
        'inputs': [{
            'name': '_expiration',
            'type': 'uint256'
        }, {
            'name': '_hash',
            'type': 'bytes20'
        }, {
            'name': '_participant',
            'type': 'address'
        }],
        'name': 'initiate',
        'outputs': [],
        'payable': True,
        'stateMutability': 'payable',
        'type': 'function'
    }, {
        'constant': False,
        'inputs': [{
            'name': '_secret',
            'type': 'bytes32'
        }],
        'name': 'redeem',
        'outputs': [],
        'payable': False,
        'stateMutability': 'nonpayable',
        'type': 'function'
    }]


class EthereumTestnet(Ethereum):

    name = 'test-ethereum'
    infura_network = 'kovan'
    tokens = kovan_tokens
    token_class = EthereumTestnetToken
    testnet = True
    etherscan_api_subdomain = 'api-kovan'

    contract_address = '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8'
