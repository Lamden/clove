from clove.network import Ethereum, EthereumTestnet


class TokenMixin(object):

    abi = [{
        "constant": False,
        "inputs": [{
            "name": "_expiration",
            "type": "uint256"
        }, {
            "name": "_hash",
            "type": "bytes20"
        }, {
            "name": "_participant",
            "type": "address"
        }, {
            "name": "_token",
            "type": "address"
        }, {
            "name": "_value",
            "type": "uint256"
        }],
        "name": "initiate",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }, {
        "constant": False,
        "inputs": [{
            "name": "_hash",
            "type": "bytes20"
        }],
        "name": "refund",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }, {
        "constant": False,
        "inputs": [{
            "name": "_secret",
            "type": "bytes32"
        }],
        "name": "redeem",
        "outputs": [],
        "payable": False,
        "stateMutability": "nonpayable",
        "type": "function"
    }]
    token_address = None

    @classmethod
    def from_namedtuple(cls, token):
        token_instance = cls()
        token_instance.symbols = (token.symbol, )
        token_instance.token_address = token.address
        token_instance.name = token.name
        return token_instance


class EthereumToken(Ethereum, TokenMixin):

    pass


class EthereumTestnetToken(EthereumTestnet, TokenMixin):

    contract_address = '0x7657Ca877Fac31D20528B473162E39B6E152fd2e'
