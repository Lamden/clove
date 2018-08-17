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

BLOCKCYPHER_SUPPORTED_NETWORKS = (
    'btc', 'doge', 'dash'
)

CRYPTOID_SUPPORTED_NETWORKS = (
    '1337', '2give', '42', '8bit', 'abc', 'ac', 'adc', 'aeg', 'anc', 'arco',
    'arg', 'atms', 'atom', 'b3', 'bash', 'bay', 'bcc', 'bee2', 'bela', 'bitb',
    'blitz', 'blk', 'block', 'boli', 'brit', 'bro', 'bsd', 'bta', 'btc', 'btci',
    'btd', 'btdx', 'btg', 'btm', 'btx', 'bucks', 'bxt', 'byc', 'byz', 'bzl',
    'cach', 'cann', 'c2', 'carbon', 'cbx', 'ccc', 'ccn', 'chao', 'chbt', 'civ',
    'club', 'cnc', 'cno', 'colx', 'corg', 'cpc', 'cqst', 'crea', 'crypt',
    'crw', 'cure', 'dash', 'dgb', 'dgc', 'dime', 'dmd', 'dmx', 'dnr', 'dollar',
    'dope', 'dot', 'drs', 'drz', 'dtc', 'dvc', 'eac', 'ebc', 'ec', 'ecc',
    'ecn', 'efl', 'egc', 'egcc', 'emc2', 'emd', 'enrg', 'ent', 'eqt', 'erc',
    'ery', 'fail', 'flax', 'fuel', 'funk', 'gam', 'gap', 'gcr', 'geo', 'glc',
    'gld', 'gre', 'grn', 'grs', 'grs-test', 'gun', 'hbn', 'hxx', 'i0c', 'icn',
    'imx', 'info', 'infx', 'insn', 'ioc', 'ion', 'itc', 'ivc', 'ixc', 'j',
    'karm', 'klk', 'knc', 'kobo', 'kore', 'koruna', 'kush', 'lana', 'lems',
    'lir', 'lol', 'loc', 'ltc', 'lux', 'linx', 'ltca', 'mac', 'manna', 'max',
    'maxt', 'may', 'mbch', 'mec', 'meow', 'mnd', 'mojo3', 'moon', 'mscn',
    'mst', 'mue', 'nav', 'ned', 'neos', 'netko', 'neva', 'nobl', 'note', 'npc',
    'nro', 'nxx', 'oc', 'octo', 'off', 'ok', 'opal', 'ozc', 'pak', 'part',
    'pho', 'phr', 'piggy', 'pink', 'pivx', 'pnd', 'poker', 'post', 'pot',
    'ppc', 'ppc-test', 'pr', 'psb', 'ptc', 'pura', 'put', 'pxi', 'pwc', 'qrk',
    'rads', 'rads-test', 'rbc', 'rby', 'ric', 'rns', 'rsgp', 'scol', 'sfr',
    'sh', 'sha', 'skc', 'slg', 'slr', 'smly', 'snrg', 'spr', 'sprts', 'spz',
    'src', 'stk', 'strat', 'strat-test', 'stv', 'super', 'sync', 'swift',
    'swing', 'sxc', 'sys', 'szc', 'taj', 'talk', 'tech', 'tes', 'toa', 'tpwr',
    'troll', 'trump', 'trust', 'tx', 'tzc', 'ubiq', 'ufo', 'uni', 'uno', 'usc',
    'vash', 'vgs', 'via', 'visio', 'vivo', 'vlx', 'vrc', 'vrm', 'vtc', 'vuc',
    'wac', 'wbc', 'wc', 'wc-old', 'wex', 'worm', 'wsx', 'wyv', 'ww', 'x2c',
    'xc', 'xcs', 'xjo', 'xlr', 'xmg', 'xmy', 'xp', 'xpy', 'xqn', 'xspec',
    'xst', 'xstc', 'xto', 'xvp', 'xzc', 'zeit', 'zet', 'zoi'
)

NETWORKS_WITH_API = BLOCKCYPHER_SUPPORTED_NETWORKS + CRYPTOID_SUPPORTED_NETWORKS

ETH_REDEEM_GAS_LIMIT = 100000
ETH_REFUND_GAS_LIMIT = 100000

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
