from hexbytes.main import HexBytes
from web3.utils.datastructures import AttributeDict

eth_initial_transaction = AttributeDict({
    'blockHash': HexBytes('0xebb8d4e62dc5b0732bee6e2c3946c5a972988f41fbac321eb73311930a936804'),
    'blockNumber': 6600435,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'gas': 126221,
    'gasPrice': 14959965017,
    'hash': HexBytes('0x7221773115ded91f856cedb2032a529edabe0bab8785d07d901681512314ef41'),
    'input': (
        '0xeb8ae1ed000000000000000000000000000000000000000000000000000000005abe25ea10ff9'
        '72f3d8181f603aa7f6b4bc172de730fec2b00000000000000000000000000000000000000000000'
        '0000d867f293ba129629a9f9355fa285b8d3711a9092'
    ),
    'nonce': 16,
    'publicKey': HexBytes(
        '0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adcb150e521'
        '6213bc301f3a6b71a178c81ddd34a361d696c8cb03970590d4f'
    ),
    'r': HexBytes('0x7a4e11ea96640fb0ab255960cea6afcf16732246ce1dadeec52eb6a8d59c2e05'),
    'raw': HexBytes(
        '0xf8ca1085037baef3598301ed0d949f7e5402ed0858ea0c5914d44b900a42c89547b80cb864eb8'
        'ae1ed000000000000000000000000000000000000000000000000000000005abe25ea10ff972f3d'
        '8181f603aa7f6b4bc172de730fec2b000000000000000000000000000000000000000000000000d'
        '867f293ba129629a9f9355fa285b8d3711a90921ba07a4e11ea96640fb0ab255960cea6afcf1673'
        '2246ce1dadeec52eb6a8d59c2e05a06f47ffe2bc88915013295be61c503bc52762fe4f7826fa249'
        '0b2d302a11bff85'
    ),
    's': HexBytes('0x6f47ffe2bc88915013295be61c503bc52762fe4f7826fa2490b2d302a11bff85'),
    'standardV': 0,
    'to': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'transactionIndex': 0,
    'v': 27,
    'value': 12
})

eth_unsupported_transaction = AttributeDict({
    'input': (
        '0xeb7ae1ed000000000000000000000000000000000000000000000000000000005abe25ea10ff9'
        '72f3d8181f603aa7f6b4bc172de730fec2b00000000000000000000000000000000000000000000'
        '0000d867f293ba129629a9f9355fa285b8d3711a9092'
    ),
})

eth_redeem_tranaction = AttributeDict({
    'blockHash': HexBytes('0x4a1f01ed71161e103d0fc4a82ec2facdc1b685e3a597fca07bb9b822b74ed686'),
    'blockNumber': 6612187,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'gas': 100000,
    'gasPrice': 1000000000,
    'hash': HexBytes('0x89b0d28e93ce55da4adab989cd48a524402eb154b23e1777f82e715589aba317'),
    'input': '0xeda1122c1e5a567ab04cc900c3da01d1b61c1a3755d648410963c3d0767ed2e0138e03a1',
    'nonce': 14,
    'publicKey': HexBytes(
        '0x579c6126677857d4d5a227ed47efbd9742e26f60449e8ea6a536c0dd9b2fb6f'
        'b14e0fddc7cb06fd78d2c6c3ef4d1b72e488096504817ed7ac252b2453cbfab56'
    ),
    'r': HexBytes('0x9ca27c2d31c663c0202851eea34e39b90311173916101bf3c3437f0fa23e54e9'),
    'raw': HexBytes(
        '0xf8880e843b9aca00830186a0949f7e5402ed0858ea0c5914d44b900a42c8954'
        '7b880a4eda1122c1e5a567ab04cc900c3da01d1b61c1a3755d648410963c3d076'
        '7ed2e0138e03a11ca09ca27c2d31c663c0202851eea34e39b90311173916101bf'
        '3c3437f0fa23e54e9a022ae2c66a04f526f17d6cbb2bf873fbbb5c3bf68bfdebf'
        'd08fbdd2b9088283a0'
    ),
    's': HexBytes('0x22ae2c66a04f526f17d6cbb2bf873fbbb5c3bf68bfdebfd08fbdd2b9088283a0'),
    'standardV': 1,
    'to': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'transactionIndex': 3,
    'v': 28,
    'value': 0,
})

token_initial_transaction = AttributeDict({
    'blockHash': HexBytes('0x2d10ee8f6d5b809cdcd52994a5d80829b3b431ac2353abd09905c144304e6c24'),
    'blockNumber': 6632638,
    'chainId': None,
    'condition': None,
    'creates': None,
    'from': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'gas': 1000000,
    'gasPrice': 2000000000,
    'hash': HexBytes('0x316d3aaa252adb025c3486cf83949245f3f10edc169e1eb0772ed074fddb8be6'),
    'input': '0x52f50db700000000000000000000000000000000000000000000000000000000'
             '5ac0e7e406821b98736162c1b007155e818536ec5fd57950000000000000000000'
             '000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a'
             '909200000000000000000000000053e546387a0d054e7ff127923254c0a679da6d'
             'bf0000000000000000000000000000000000000000000000000000000000000064',
    'nonce': 25,
    'publicKey': HexBytes(
        '0x76c4f5810736d1d9b9964863abc339dce70ace058db5c820e5fdec26e0840f36f9adc'
        'b150e5216213bc301f3a6b71a178c81ddd34a361d696c8cb03970590d4f'
    ),
    'r': HexBytes('0x5d66dc1d458dc78eaa639fe425143f21a09706ede02415b7fd41a7bbb88c4da0'),
    'raw': HexBytes(
        '0xf90109198477359400830f4240947657ca877fac31d20528b473162e39b6e152fd2e80b8a452'
        'f50db7000000000000000000000000000000000000000000000000000000005ac0e7e406821b98'
        '736162c1b007155e818536ec5fd579500000000000000000000000000000000000000000000000'
        '00d867f293ba129629a9f9355fa285b8d3711a909200000000000000000000000053e546387a0d'
        '054e7ff127923254c0a679da6dbf00000000000000000000000000000000000000000000000000'
        '000000000000641ca05d66dc1d458dc78eaa639fe425143f21a09706ede02415b7fd41a7bbb88c'
        '4da0a07d2ceb71a0965ea61bcafbe86670f58c3b157d8dff456b3bca195f3d2c57d595'
    ),
    's': HexBytes('0x7d2ceb71a0965ea61bcafbe86670f58c3b157d8dff456b3bca195f3d2c57d595'),
    'standardV': 1,
    'to': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
    'transactionIndex': 0,
    'v': 28,
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
