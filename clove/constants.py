COLORED_LOGS_STYLES = {
    'info': {'color': 'green'},
    'error': {'color': 'red'},
    'debug': {'color': 'magenta'},
    'warning': {'color': 'yellow'}
}
NODE_COMMUNICATION_TIMEOUT = 2 * 60
TRANSACTION_BROADCASTING_MAX_ATTEMPTS = 10

SIGNATURE_SIZE = 110

# How many seconds should we wait for the reject message to appear
# after publishing transaction
REJECT_TIMEOUT = 10

CLOVE_API_URL = 'https://clove-api.lamden.io'

ETH_REDEEM_GAS_LIMIT = 100000
ETH_REFUND_GAS_LIMIT = 100000

ETH_FILTER_MAX_ATTEMPTS = 10

ERC20_BASIC_ABI = [{
    "constant": True,
    "inputs": [],
    "name": "symbol",
    "outputs": [{
        "name": "",
        "type": "string"
    }],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
}, {
    "constant": True,
    "inputs": [],
    "name": "name",
    "outputs": [{
        "name": "",
        "type": "string"
    }],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
}, {
    "constant": True,
    "inputs": [],
    "name": "decimals",
    "outputs": [{
        "name": "",
        "type": "uint8"
    }],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
}]


ETHEREUM_CONTRACT_ABI = [{
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
            "name": "_isToken",
            "type": "bool"
        }, {
            "name": "_value",
            "type": "uint256"
    }],
    "name": "initiate",
    "outputs": [],
    "payable":True,
    "stateMutability": "payable",
    "type": "function"
}, {
    "constant": True,
    "inputs": [{
        "name": "",
        "type": "address"
    }, {
        "name": "",
        "type": "bytes20"
    }],
    "name": "swaps",
    "outputs": [{
        "name": "expiration",
        "type": "uint256"
    }, {
        "name": "initiator",
        "type": "address"
    }, {
        "name": "participant",
        "type": "address"
    }, {
        "name": "value",
        "type": "uint256"
    }, {
        "name": "isToken",
        "type": "bool"
    }, {
        "name": "token",
        "type": "address"
    }, {
        "name": "exists",
        "type": "bool"
    }],
    "payable": False,
    "stateMutability": "view",
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
}, {
    "constant": False,
    "inputs": [{
        "name": "_hash",
        "type": "bytes20"
    }, {
        "name": "_participant",
        "type": "address"
    }],
    "name": "refund",
    "outputs": [],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
}, {
    "anonymous": False,
    "inputs": [{
        "indexed": False,
        "name": "_initiator",
        "type": "address"
    }, {
        "indexed": False,
        "name": "_participant",
        "type": "address"
    }, {
        "indexed": False,
        "name": "_expiration",
        "type": "uint256"
    }, {
        "indexed": False,
        "name": "_hash",
        "type": "bytes20"
    }, {
        "indexed": False,
        "name": "_token",
        "type": "address"
    }, {
        "indexed": False,
        "name": "_isToken",
        "type": "bool"
    }, {
        "indexed": False,
        "name": "_value",
        "type": "uint256"
    }],
    "name": "InitiateSwap",
    "type": "event"
}, {
    "anonymous": False,
    "inputs": [{
        "indexed": False,
        "name": "_participant",
        "type": "address"
    }, {
        "indexed": False,
        "name": "_hash",
        "type": "bytes20"
    }, {
        "indexed": False,
        "name": "_secret",
        "type": "bytes32"
    }],
    "name": "RedeemSwap",
    "type": "event"
}, {
    "anonymous": False,
    "inputs": [{
        "indexed": False,
        "name": "_initiator",
        "type": "address"
    }, {
        "indexed": False,
        "name": "_participant",
        "type": "address"
    }, {
        "indexed": False,
        "name": "_hash",
        "type": "bytes20"
    }],
    "name": "RefundSwap",
    "type": "event"
}]
