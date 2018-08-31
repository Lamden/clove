from hexbytes.main import HexBytes
from web3.utils.datastructures import AttributeDict

eth_initial_transaction = AttributeDict({
    'blockHash': HexBytes('0x111346453964a0df4fcd50ac759231f4f90a858c6ab62255e7c75089b22b0b40'),
    'blockNumber': 8388823,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'gas': 140502,
    'gasPrice': 1000000000,
    'hash': HexBytes('0xcf64ef4d0449cf7a78d2be1c1f7225dffb11dded98a58d569ebcc6e883ce9f2b'),
    'input': '0x7337c993000000000000000000000000000000000000000000000000000000005b782cfaed2e6fe492005de2dd82e84d38448'
             '467d632e81c000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a90920000'
             '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
             '0000000000000000000000000000000000000000000000000000000000000000000000000000000000000',
    'nonce': 283,
    'publicKey': HexBytes(
        '0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adcb150e5216213bc301f3a6b71a178'
        'c81ddd34a361d696c8cb03970590d4f'
    ),
    'r': HexBytes('0x68e2bbdd4cb4e989854a87aa8964c65b3bf28f68183f73f905ab8841db690cbb'),
    'raw': HexBytes(
        '0xf9013282011b843b9aca00830224d694ce07ab9477bc20790b88b398a2a9e0f626c7d26387038d7ea4c68000b8c47337c993000000'
        '000000000000000000000000000000000000000000000000005b782cfaed2e6fe492005de2dd82e84d38448467d632e81c0000000000'
        '00000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a9092000000000000000000000000000000'
        '000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
        '0000000000000000000000000000000000000000000000000000001ca068e2bbdd4cb4e989854a87aa8964c65b3bf28f68183f73f905'
        'ab8841db690cbba0227712dc5c204041cc8c44facac023c457725acc905b2db311b1176cd53836e0'
    ),
    's': HexBytes('0x227712dc5c204041cc8c44facac023c457725acc905b2db311b1176cd53836e0'),
    'standardV': 1,
    'to': '0xce07aB9477BC20790B88B398A2A9e0F626c7D263',
    'transactionIndex': 1,
    'v': 28,
    'value': 1000000000000000
})

eth_unsupported_transaction = AttributeDict({
    'input': (
        '0xeb7ae1ed000000000000000000000000000000000000000000000000000000005abe25ea10ff9'
        '72f3d8181f603aa7f6b4bc172de730fec2b00000000000000000000000000000000000000000000'
        '0000d867f293ba129629a9f9355fa285b8d3711a9092'
    ),
})

eth_redeem_tranaction = AttributeDict({
    'blockHash': HexBytes('0x579c835eb257089492b99c44aae33660cd5efd83297036a4d0d6c11c8921ae8c'),
    'blockNumber': 8398155,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'gas': 100000,
    'gasPrice': 2000000000,
    'hash': HexBytes('0x65320e57b9d18ec08388896b029ad1495beb7a57c547440253a1dde01b4485f1'),
    'input': '0xeda1122cbc2424e1dcdd2e425c555bcea35a54fd27cf540e60f18366e153e3fb7cf4490c',
    'nonce': 146,
    'publicKey': HexBytes(
        '0x579c6126677857d4d5a227ed47efbd9742e26f60449e8ea6a536c0dd9b2fb6fb14e0fddc7cb06fd78d2c6c3ef4d1b72e48809650'
        '4817ed7ac252b2453cbfab56'
    ),
    'r': HexBytes('0xcde19e4d2d78e196ecc8dff5ba6e2c90bfc6be93241e8dd2584734e870e6b677'),
    'raw': HexBytes(
        '0xf88981928477359400830186a094ce07ab9477bc20790b88b398a2a9e0f626c7d26380a4eda1122cbc2424e1dcdd2e425c555bce'
        'a35a54fd27cf540e60f18366e153e3fb7cf4490c1ba0cde19e4d2d78e196ecc8dff5ba6e2c90bfc6be93241e8dd2584734e870e6b6'
        '77a02fe805af66d13352198a8b19b53ee1dc27671b76a4626af8cead8211537ea7d9'
    ),
    's': HexBytes('0x2fe805af66d13352198a8b19b53ee1dc27671b76a4626af8cead8211537ea7d9'),
    'standardV': 0,
    'to': '0xce07aB9477BC20790B88B398A2A9e0F626c7D263',
    'transactionIndex': 0,
    'v': 27,
    'value': 0
})

token_initial_transaction = AttributeDict({
    'blockHash': HexBytes('0x0cc3bd2154a33a91362ff719c1f891aac2e3bb5ecd298878dd08bbd6c562a9e4'),
    'blockNumber': 8399513,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'gas': 180590,
    'gasPrice': 1000000000,
    'hash': HexBytes('0x224818e4390e6d4e24b18e19a268825c0bbc649ab3e93dcb446328973dc7914b'),
    'input': '0x7337c993000000000000000000000000000000000000000000000000000000005b7962b834378f0187488d019d3e0151f2fe'
             '3d3672ca310e000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a909200'
             '000000000000000000000053e546387a0d054e7ff127923254c0a679da6dbf0000000000000000000000000000000000000000'
             '00000000000000000000000100000000000000000000000000000000000000000000003635c9adc5dea00000',
    'nonce': 287,
    'publicKey': HexBytes(
        '0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adcb150e5216213bc301f3a6b71a178c81ddd34'
        'a361d696c8cb03970590d4f'
    ),
    'r': HexBytes('0xe184d8b211a07bd1fea3f7b373e18624e2973db797f512c004cf3dd131994fce'),
    'raw': HexBytes(
        '0xf9012b82011f843b9aca008302c16e94ce07ab9477bc20790b88b398a2a9e0f626c7d26380b8c47337c9930000000000000000000'
        '00000000000000000000000000000000000005b7962b834378f0187488d019d3e0151f2fe3d3672ca310e0000000000000000000000'
        '00000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a909200000000000000000000000053e546387a0d054e7'
        'ff127923254c0a679da6dbf000000000000000000000000000000000000000000000000000000000000000100000000000000000000'
        '000000000000000000000000003635c9adc5dea000001ba0e184d8b211a07bd1fea3f7b373e18624e2973db797f512c004cf3dd1319'
        '94fcea05bc5daa0d693604f2c645ed7d7cfa53f6ebe8f4f6bb3e45a98f57946050a5503'
    ),
    's': HexBytes('0x5bc5daa0d693604f2c645ed7d7cfa53f6ebe8f4f6bb3e45a98f57946050a5503'),
    'standardV': 0,
    'to': '0xce07aB9477BC20790B88B398A2A9e0F626c7D263',
    'transactionIndex': 11,
    'v': 27,
    'value': 0
})


etherscan_internal_transactions = {
    "message": "OK",
    "result": [
        {
            "blockNumber": "6628836",
            "contractAddress": "",
            "errCode": "",
            "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
            "gas": "2300",
            "gasUsed": "0",
            "hash": "0x862b393fd64d4c1ae1a6cc55f2c6f36a87fdce46dcc7abb1a7ba174c10bb0281",
            "input": "",
            "isError": "0",
            "timeStamp": "1522398684",
            "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
            "traceId": "0",
            "type": "call",
            "value": "8"
        },
        {
            "blockNumber": "6712309",
            "contractAddress": "",
            "errCode": "",
            "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
            "gas": "2300",
            "gasUsed": "0",
            "hash": "0x2dd60f28a3ef781fd12adfeb3b622fe424a268816392bbac4d5116ead94a0fde",
            "input": "",
            "isError": "0",
            "timeStamp": "1522841088",
            "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
            "traceId": "0",
            "type": "call",
            "value": "1"
        },
        {
            "blockNumber": "6793058",
            "contractAddress": "",
            "errCode": "",
            "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
            "gas": "2300",
            "gasUsed": "0",
            "hash": "0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1",
            "input": "",
            "isError": "0",
            "timeStamp": "1523275524",
            "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
            "traceId": "0",
            "type": "call",
            "value": "500000000000000000"
        },
        {
            "blockNumber": "6795065",
            "contractAddress": "",
            "errCode": "",
            "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
            "gas": "2300",
            "gasUsed": "0",
            "hash": "0x4c21cf7bb5d64f659ba02f84e9af42150d7911147588a2b5fe4330f73d6afb33",
            "input": "",
            "isError": "0",
            "timeStamp": "1523285852",
            "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
            "traceId": "0",
            "type": "call",
            "value": "9"
        },
        {
            "blockNumber": "6837685",
            "contractAddress": "",
            "errCode": "",
            "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
            "gas": "2300",
            "gasUsed": "0",
            "hash": "0xbf0b86b80ca9780c7e992c9c5bf5fc8db75e434821fc0a51545e469f554f9878",
            "input": "",
            "isError": "0",
            "timeStamp": "1523530744",
            "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
            "traceId": "0",
            "type": "call",
            "value": "1000000000000000000"
        },
        {
            "blockNumber": "6896101",
            "contractAddress": "",
            "errCode": "",
            "from": "0x9f7e5402ed0858ea0c5914d44b900a42c89547b8",
            "gas": "2300",
            "gasUsed": "0",
            "hash": "0xadded643661b566661969bb05dc3aa25eaa3ad6eef371d01e3af3e9386c266a9",
            "input": "",
            "isError": "0",
            "timeStamp": "1523951692",
            "to": "0x999f348959e611f1e9eab2927c21e88e48e6ef45",
            "traceId": "0",
            "type": "call",
            "value": "1000000000000000000"
        },
        {
            "blockNumber": "8398155",
            "timeStamp": "1534499184",
            "hash": "0x65320e57b9d18ec08388896b029ad1495beb7a57c547440253a1dde01b4485f1",
            "from": "0xce07ab9477bc20790b88b398a2a9e0f626c7d263",
            "to": "0xd867f293ba129629a9f9355fa285b8d3711a9092",
            "value": "1000000000000000",
            "contractAddress": "",
            "input": "",
            "type": "call",
            "gas": "2300",
            "gasUsed": "0",
            "traceId": "0",
            "isError": "0",
            "errCode": ""
        }
    ],
    "status": "1"
}


etherscan_token_transfers = {
    'message': 'OK',
    'result': [
        {
            'blockHash': '0x2ef27e7756085092110f12cb8f2afe76c880ccbb2671e1031acce2b95817a5b8',
            'blockNumber': '6632744',
            'confirmations': '378903',
            'contractAddress': '0x53e546387a0d054e7ff127923254c0a679da6dbf',
            'cumulativeGasUsed': '1241085',
            'from': '0x7657ca877fac31d20528b473162e39b6e152fd2e',
            'gas': '100000',
            'gasPrice': '2000000000',
            'gasUsed': '31318',
            'hash': '0x66ffdb539975eb20f191771ad8363ae0b733d55dde670050fbff35083b243365',
            'input': '0xeda1122c6d503d17aa32ee13626cd21f2b4b7fffb0f0dae8d2ebe03b67f71b6a0ac8059c',
            'nonce': '16',
            'timeStamp': '1522419468',
            'to': '0xd867f293ba129629a9f9355fa285b8d3711a9092',
            'tokenDecimal': '18',
            'tokenName': 'BlockbustersTest',
            'tokenSymbol': 'BBT',
            'transactionIndex': '2',
            'value': '100'
        }, {
            'blockHash': '0x567dd4c3278e127a373737756900eee2f8f026872105a31dab90e430ce6f044a',
            'blockNumber': '6729432',
            'confirmations': '282215',
            'contractAddress': '0x53e546387a0d054e7ff127923254c0a679da6dbf',
            'cumulativeGasUsed': '23159',
            'from': '0x7657ca877fac31d20528b473162e39b6e152fd2e',
            'gas': '100000',
            'gasPrice': '1502509001',
            'gasUsed': '23159',
            'hash': '0xe9cdd7268e74585541a30ed5cdd833034b1000b2214ce1cebd992f4aa2bb9594',
            'input': '0xeda1122cde05b3ecfe71cde5b3de7f4a25f71397c7fd523ce75dcf15c772f75e9149e369',
            'nonce': '17',
            'timeStamp': '1522934116',
            'to': '0xd867f293ba129629a9f9355fa285b8d3711a9092',
            'tokenDecimal': '18',
            'tokenName': 'BlockbustersTest',
            'tokenSymbol': 'BBT',
            'transactionIndex': '0',
            'value': '1000'
        }, {
            'blockHash': '0x29c99068878c7b5ce5b0f463611286b5b9b26bfff71cbcddd75bfb3733cc7057',
            'blockNumber': '6793658',
            'confirmations': '217989',
            'contractAddress': '0x53e546387a0d054e7ff127923254c0a679da6dbf',
            'cumulativeGasUsed': '23127',
            'from': '0x7657ca877fac31d20528b473162e39b6e152fd2e',
            'gas': '100000',
            'gasPrice': '20000000000',
            'gasUsed': '23127',
            'hash': '0x4fd41289b816f6122e59a0759bd10441ead75d550562f4b3aad2fddc56eb3274',
            'input': '0xeda1122cc037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac',
            'nonce': '19',
            'timeStamp': '1523278616',
            'to': '0xd867f293ba129629a9f9355fa285b8d3711a9092',
            'tokenDecimal': '18',
            'tokenName': 'BlockbustersTest',
            'tokenSymbol': 'BBT',
            'transactionIndex': '0',
            'value': '1000000000000000000000'
        }, {
            'blockHash': '0x7cc3ab91379594c4af17ecc6a25422a59777ebfb2977fd7cad1332657c020e5c',
            'blockNumber': '7009010',
            'confirmations': '2637',
            'contractAddress': '0x53e546387a0d054e7ff127923254c0a679da6dbf',
            'cumulativeGasUsed': '284596',
            'from': '0x7657ca877fac31d20528b473162e39b6e152fd2e',
            'gas': '100000',
            'gasPrice': '24074000000',
            'gasUsed': '31318',
            'hash': '0x329f4bffbb5385bec8816740c5e423a91b89583e6952b16b644a48157f556269',
            'input': '0xeda1122c371e3ef7b06f29766252344219697fbeedc15e62711fbc258a2e71d5cb59d048',
            'nonce': '24',
            'timeStamp': '1524734944',
            'to': '0xd867f293ba129629a9f9355fa285b8d3711a9092',
            'tokenDecimal': '18',
            'tokenName': 'BlockbustersTest',
            'tokenSymbol': 'BBT',
            'transactionIndex': '1',
            'value': '600000000000000000'
        },
        {
            "blockNumber": "8399524",
            "timeStamp": "1534509088",
            "hash": "0xda110a95189e069b34dacbde2594093f2cc303d652c21ed0ce57fd953546fb6f",
            "nonce": "147",
            "blockHash": "0x26b3530fa72d0fb48d15accbaa4059d67eef02f9cd9139cf9bde1d3157700eac",
            "from": "0xce07ab9477bc20790b88b398a2a9e0f626c7d263",
            "contractAddress": "0x53e546387a0d054e7ff127923254c0a679da6dbf",
            "to": "0xd867f293ba129629a9f9355fa285b8d3711a9092",
            "value": "1000000000000000000000",
            "tokenName": "BlockbustersTest",
            "tokenSymbol": "BBT",
            "tokenDecimal": "18",
            "transactionIndex": "4",
            "gas": "100000",
            "gasPrice": "1000000000",
            "gasUsed": "33766",
            "cumulativeGasUsed": "490865",
            "input": "0xeda1122c3c76e1e7e2b7b7e701e31c418af3f79cb01a9192155394629fd085ef422116e7",
            "confirmations": "1054"
        }
    ],
    'status': '1'
}


eth_contract = AttributeDict({
    'blockHash': HexBytes('0x9c581f507f5541fba0d5e3d897e46dcdffab497d59987ebe0337f89581e4d8cd'),
    'blockNumber': 6792738,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'gas': 126221,
    'gasPrice': 20000000000,
    'hash': HexBytes('0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f'),
    'input': (
        '0xeb8ae1ed000000000000000000000000000000000000000000000000000000005acca1d68cebcb1af6fa5fddeb'
        '091f61f0af1c49a6de9922000000000000000000000000000000000000000000000000999f348959e611f1e9eab2'
        '927c21e88e48e6ef45'
    ),
    'nonce': 18,
    'publicKey': HexBytes(
        '0x579c6126677857d4d5a227ed47efbd9742e26f60449e8ea6a536c0dd9b2fb6fb14e0fddc7cb06fd78d2c6c3ef4'
        'd1b72e488096504817ed7ac252b2453cbfab56'
    ),
    'r': HexBytes('0x165e3e1c366078a77491348daf306b9b2e9e2a2d884efb0c750fa9d701009b75'),
    'raw': HexBytes(
        '0xf8d2128504a817c8008301ed0d949f7e5402ed0858ea0c5914d44b900a42c89547b88806f05b59d3b20000b864'
        'eb8ae1ed000000000000000000000000000000000000000000000000000000005acca1d68cebcb1af6fa5fddeb09'
        '1f61f0af1c49a6de9922000000000000000000000000000000000000000000000000999f348959e611f1e9eab292'
        '7c21e88e48e6ef451ca0165e3e1c366078a77491348daf306b9b2e9e2a2d884efb0c750fa9d701009b75a04c6672'
        '33a3f4570964c58a0e145f3ace761315c05a0b8360fefe2b67f8e00eba'
    ),
    's': HexBytes('0x4c667233a3f4570964c58a0e145f3ace761315c05a0b8360fefe2b67f8e00eba'),
    'standardV': 1,
    'to': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'transactionIndex': 1,
    'v': 28,
    'value': 500000000000000000,
})


eth_token_contract = AttributeDict({
    'blockHash': HexBytes('0x463fd37f1623fb9d7e16b341929e83a8bbb6b946c8674f29fb948f9f7f1a73dc'),
    'blockNumber': 6998035,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'gas': 300000,
    'gasPrice': 4000000000,
    'hash': HexBytes('0x270cc74bf60fd0d37806b000a11da972ce240fa7478e38d8b44b6793ddd3284d'),
    'input': (
        '0x52f50db7000000000000000000000000000000000000000000000000000000005ae3085f7780c856405b3ce2e2c'
        '717857b3439c545316974000000000000000000000000000000000000000000000000d867f293ba129629a9f9355f'
        'a285b8d3711a909200000000000000000000000053e546387a0d054e7ff127923254c0a679da6dbf0000000000000'
        '000000000000000000000000000000000000853a0d2313c0000'
    ),
    'nonce': 58,
    'publicKey': HexBytes(
        '0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adcb150e5216213bc301f3a6b'
        '71a178c81ddd34a361d696c8cb03970590d4f'
    ),
    'r': HexBytes('0x579ab66e7cab564d9c67e50c571b1e36afe0095d9d539d4cd3dd871893316201'),
    'raw': HexBytes(
        '0xf901093a84ee6b2800830493e0947657ca877fac31d20528b473162e39b6e152fd2e80b8a452f50db7000000000'
        '000000000000000000000000000000000000000000000005ae3085f7780c856405b3ce2e2c717857b3439c5453169'
        '74000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a9092000'
        '00000000000000000000053e546387a0d054e7ff127923254c0a679da6dbf00000000000000000000000000000000'
        '00000000000000000853a0d2313c00001ba0579ab66e7cab564d9c67e50c571b1e36afe0095d9d539d4cd3dd87189'
        '3316201a05a1a325b46b19eb5f43a2989daf5c92aac1ca48187866a3268ff47cc4e88911e'
    ),
    's': HexBytes('0x5a1a325b46b19eb5f43a2989daf5c92aac1ca48187866a3268ff47cc4e88911e'),
    'standardV': 0,
    'to': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
    'transactionIndex': 0,
    'v': 27,
    'value': 0
})


eth_raw_unsigned_transaction = '0xf86880843b9aca0082b2089453e546387a0d054e7ff127923254c' \
                               '0a679da6dbf80b844095ea7b30000000000000000000000007657ca' \
                               '877fac31d20528b473162e39b6e152fd2e000000000000000000000' \
                               '00000000000000000000000003635c9adc5dea00000808080'
