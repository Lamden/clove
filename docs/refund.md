# Transaction refunds

Atomic swaps work because if any party does not comply with the previously agreed upon terms, the transaction can revert using a refund mechanism.

## Bitcoin based networks

#### Here are some examples of transaction refunds.

### I Initial transaction refund

Alice created and published such transaction:

    {'contract': '63a61446260875cb8c88ba918cdd913ae23c59562f95298876a9141a376f6634e41c22b28bc9ef3336a623717083a46704396b645bb17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac',
    'contract_address': '3KLY8YnMbcWqkNdSmtgwZVxx6hpU4AWFX6',
    'contract_transaction': '0100000001e4f0bb83bc3b52f921ad9d064768ba1702d9ec92befa3529a17e5163c90a11a0010000008a47304402202c8e3c6814938dae17c02125990cadd550edee97df9529f889639f4096f55fe4022060cf5b36a0a3b103ae705937a65903710b849296076ce010c61da48e0946b1ad0141044fbe9cf6ef9bf4a13a693ee1d431eb700a592e8097619e0cfe82aff2a5c231e7154e464e4ec94201007b403b6de9a5819b0bc31eef0741c4fe6e932bca6d9cca0000000002001bb7000000000017a914c192be92fa15e5a97cfeae84fb2ac830594ea9fb8780795209000000001976a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac00000000',
    'transaction_address': '1f317ce1ab1c7504d5e70cac4cb97f6e41fbaded4dd1f094d431a9f0a508ab44',
    'fee': 0.001,
    'fee_per_kb': 0.0,
    'fee_per_kb_text': '0.00000000 MONA / 1 kB',
    'fee_text': '0.00100000 MONA',
    'locktime': datetime.datetime(2018, 8, 3, 14, 48, 25, 29266),
    'recipient_address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
    'refund_address': 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ',
    'secret': '41029c8c094a3d747f99e3b6960c6df1e5defaa81dfe961be6f3cae9755a6c3d',
    'secret_hash': '46260875cb8c88ba918cdd913ae23c59562f9529',
    'size': 255,
    'size_text': '255 bytes',
    'value': 0.12,
    'value_text': '0.12000000 MONA'}


She was waiting for the response from Bob for a day but she did not receive any,
so she decided to refund the money from the blockchain:

### 1. Get a wallet from the newtork

    from clove.network import Monacoin

    mona_network = Monacoin()

    alice_mona_wallet = mona_network.get_wallet(private_key='aliceprivatekey') # provide real key

    alice_mona_wallet.address
    'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ'

### 2. Create refund transaction

    alice_contract = mona_network.audit_contract(
        contract='63a61446260875cb8c88ba918cdd913ae23c59562f95298876a9141a376f6634e41c22b28bc9ef3336a623717083a46704396b645bb17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac',
        raw_transaction='0100000001e4f0bb83bc3b52f921ad9d064768ba1702d9ec92befa3529a17e5163c90a11a0010000008a47304402202c8e3c6814938dae17c02125990cadd550edee97df9529f889639f4096f55fe4022060cf5b36a0a3b103ae705937a65903710b849296076ce010c61da48e0946b1ad0141044fbe9cf6ef9bf4a13a693ee1d431eb700a592e8097619e0cfe82aff2a5c231e7154e464e4ec94201007b403b6de9a5819b0bc31eef0741c4fe6e932bca6d9cca0000000002001bb7000000000017a914c192be92fa15e5a97cfeae84fb2ac830594ea9fb8780795209000000001976a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac00000000'
    )

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs contract audit can be done based on contract and transaction hash.
See an exmaple in [participate refund](#2-create-refund-transaction-1).

Alice refunds the contract.

    refund_transaction = alice_contract.refund(alice_mona_wallet)
    RuntimeError: This contract is still valid! It can't be refunded until 2018-08-03 14:48:25 UTC.

Oops! Something went wrong! Contract is still valid! Alice was a bit impatient, wasn't she?

Initial transaction contract is set to be **valid for 48 hours**.

Okey! It is past 2018-08-03 14:48:25 UTC, so Alice is free to create a refund transaction!

    refund_transaction = alice_contract.refund(alice_mona_wallet)

### 3. Sign and publish refund transaction

    refund_transaction.fee = 0.001  # As monacoin has no explorer with API we need to add fee manually
    refund_transaction.add_fee_and_sign()

    refund_transaction.show_details()
    {'fee': 0.001,
    'fee_per_kb': 0.0,
    'fee_per_kb_text': '0.00000000 MONA / 1 kB',
    'fee_text': '0.00100000 MONA',
    'recipient_address': 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ',
    'size': 308,
    'size_text': '308 bytes',
    'transaction': '010000000144ab08a5f0a931d494f0d14dedadfb416e7fb94cac0ce7d504751cabe17c311f00000000df483045022100837496713462529685110ac60e600019dff6d3a44c77f817ece5da64ca4dc42e022011b64dd743399c5c2ea7dda941a4a837d1497087e13ff6511a7e2c362c176a300141044fbe9cf6ef9bf4a13a693ee1d431eb700a592e8097619e0cfe82aff2a5c231e7154e464e4ec94201007b403b6de9a5819b0bc31eef0741c4fe6e932bca6d9cca004c5163a61446260875cb8c88ba918cdd913ae23c59562f95298876a9141a376f6634e41c22b28bc9ef3336a623717083a46704396b645bb17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac00000000016094b500000000001976a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac396b645b',
    'transaction_address': 'a5f0b7a955e606a8e54323d73e44abd608f240cb72cbad995845f2ba754a0eee',
    'value': 0.12,
    'value_text': '0.12000000 MONA'}


    refund_transaction.publish()
    'a5f0b7a955e606a8e54323d73e44abd608f240cb72cbad995845f2ba754a0eee'

### 4. Voilà! Alice should get her litecoins back. You can check it for example in a blockcypher.


### II Participate transaction refund

Bob created and published such participating transaction:

    {'contract': '63a61446260875cb8c88ba918cdd913ae23c59562f95298876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704f81b635bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
    'contract_address': 'MBtkgn1gWmm4FxAwp1WaXRtRZTfNLKTZzn',
    'contract_transaction': '0100000002505cab5a4fb315145f284ede8c43b2af3fa6557b1bfe54e46037533e6d1a5c56010000008b4830450221009c8969d08f84d39585c7181be51f692151cfe8736ca9062f4534c844987659b002205599ac2c05ea98403155ea581b169e8443904893dfd76b69e0a30fcadff9826401410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f600000000945163cde3a306cfdea2a142b63a24e1d4b7a02d6451ab55a9e9aad9ac430e961b0200008a473044022040b64bfeb8065a58ba41809e024fd9fe0ef250b3cfc6d5d92b75bf672617032d02200b1f3eb08b6a6cf3cd1b842895fe7ab218ffdbb86bdf6b473940d94786ea0c9d01410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f6000000000290ca04000000000017a9142bccd91f6a56b55cca796ef7f0aaaa33c97b25a8879db80100000000001976a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac00000000',
    'transaction_address': '40875e3889aac718594b7f9d166ca4b0c8d3fb41b25f6649429643874e8aa384',
    'fee': 0.00067565,
    'fee_per_kb': 0.00155321,
    'fee_per_kb_text': '0.00155321 LTC / 1 kB',
    'fee_text': '0.00067565 LTC',
    'locktime': datetime.datetime(2018, 8, 2, 14, 58, 0, 255583),
    'recipient_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
    'refund_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
    'secret': '',
    'secret_hash': '46260875cb8c88ba918cdd913ae23c59562f9529',
    'size': 435,
    'size_text': '435 bytes',
    'value': 0.00314,
    'value_text': '0.00314000 LTC'}


Alice didn't redeem the transaction, so no secret key was published. Bob needed to get his monacoins back.

The process is parallel as in the [initial transaction](#I-Initial-transaction-refund).

### 1. Get a wallet from the newtork

    from clove.network import Litecoin

    ltc_network = Litecoin()

    bob_ltc_wallet = ltc_network.get_wallet(private_key='bobprivatekey') # provide real key
    bob_ltc_wallet.address
    'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ'

### 2. Create refund transaction

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs contract audit can be done based on contract and transaction hash.

    bob_contract = ltc_network.audit_contract(
        contract='63a61446260875cb8c88ba918cdd913ae23c59562f95298876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704f81b635bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
        transaction_address='40875e3889aac718594b7f9d166ca4b0c8d3fb41b25f6649429643874e8aa384'
    )

For unsupported networks Bob should find the raw transaction for given transaction address by himself.

    bob_contract = ltc_network.audit_contract(
        contract='63a61446260875cb8c88ba918cdd913ae23c59562f95298876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704f81b635bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
        raw_transaction='0100000002505cab5a4fb315145f284ede8c43b2af3fa6557b1bfe54e46037533e6d1a5c56010000008b4830450221009c8969d08f84d39585c7181be51f692151cfe8736ca9062f4534c844987659b002205599ac2c05ea98403155ea581b169e8443904893dfd76b69e0a30fcadff9826401410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f600000000945163cde3a306cfdea2a142b63a24e1d4b7a02d6451ab55a9e9aad9ac430e961b0200008a473044022040b64bfeb8065a58ba41809e024fd9fe0ef250b3cfc6d5d92b75bf672617032d02200b1f3eb08b6a6cf3cd1b842895fe7ab218ffdbb86bdf6b473940d94786ea0c9d01410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f6000000000290ca04000000000017a9142bccd91f6a56b55cca796ef7f0aaaa33c97b25a8879db80100000000001976a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac00000000'
    )

Bob refunds the contract.

    refund_transaction = bob_contract.refund(bob_ltc_wallet)
    RuntimeError: This contract is still valid! It can't be refunded until 2018-08-02 14:58:00 UTC.

Oops! Something went wrong! Contract is still valid! Bob was a bit impatient, wasn't he?

Participate transaction contract is set to be **valid for 24 hours**.

Okey! It is past 2018-08-02 14:58:00 UTC, so Bob is free to create a refund transaction!

    refund_transaction = bob_contract.refund(bob_ltc_wallet)

### 3. Sign and publish refund transaction

    refund_transaction.add_fee_and_sign()

    refund_transaction.show_details()
    {'fee': 0.00051235,
    'fee_per_kb': 0.00167435,
    'fee_per_kb_text': '0.00167435 LTC / 1 kB',
    'fee_text': '0.00051235 LTC',
    'recipient_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
    'size': 308,
    'size_text': '308 bytes',
    'transaction': '010000000184a38a4e8743964249665fb241fbd3c8b0a46c169d7f4b5918c7aa89385e874000000000df4830450221009217801c3d6831631c67fd8dd19bc104e9f11a2b8d8dd4d953bba2ddf434ff530220453af8a4b8a6e6a801fcf14d8c3471ffeffa900898eda77b87d9d2be4d951e6b01410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f6004c5163a61446260875cb8c88ba918cdd913ae23c59562f95298876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704f81b635bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac00000000016d020400000000001976a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988acf81b635b',
    'transaction_address': '4e50927672b1f3921093ddf3f406a8bc91ce2509a7cff3eebfc8158282871a74',
    'value': 0.00314,
    'value_text': '0.00314000 LTC'}


     refund_transaction.publish()
     '4e50927672b1f3921093ddf3f406a8bc91ce2509a7cff3eebfc8158282871a74'

### 4. Voilà! Bob should get his monacoins back. You can check it for example [here](https://bchain.info/MONA/addr/MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ).

## Ethereum based networks

### I Initial transaction refund

Alice created and published such transaction:

    >>> initial_transaction.show_details()
    {'nonce': 249,
    'gasprice': 20000000000,
    'to': '0x7657ca877fac31d20528b473162e39b6e152fd2e',
    'value': Decimal('1000'),
    'data': '0x52f50db7000000000000000000000000000000000000000000000000000000005b59efd0f1281d5c4b4b49ac582d5ee5cd43b871309e0b28000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a909200000000000000000000000053e546387a0d054e7ff127923254c0a679da6dbf00000000000000000000000000000000000000000000003635c9adc5dea00000',
    'v': 27,
    'r': 68640564608942029631378553532061187867651305976388122732310692205381648163723,
    's': 42842279473037306433100096957396035599316452268945287098600421922947059503385,
    'sender': '0x999f348959e611f1e9eab2927c21e88e48e6ef45', '
    transaction_address': '0x209a08f2faaea4c6871cd4947293fa3fada5835e1f589fa7f0ab875a858104af',
    'gas_limit': 300000,
    'transaction': '0xf9010b81f98504a817c800830493e0947657ca877fac31d20528b473162e39b6e152fd2e80b8a452f50db7000000000000000000000000000000000000000000000000000000005b59efd0f1281d5c4b4b49ac582d5ee5cd43b871309e0b28000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a909200000000000000000000000053e546387a0d054e7ff127923254c0a679da6dbf00000000000000000000000000000000000000000000003635c9adc5dea000001ba097c12ecc5769576b447344c87e687c503390ba2e4003a209a3c4fb322b58a38ba05eb7def14f000a1ee940ffb22417b94e5ad303611e789ff438d70addc8b15119', 'recipient_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'value_text': '1000.000000000000000000 BBT',
    'secret': 'fb2cc1d75a54c2fd7d120f307442ad1051157b4759fbb92c3656e8bb639cd909',
    'secret_hash': 'f1281d5c4b4b49ac582d5ee5cd43b871309e0b28',
    'locktime': datetime.datetime(2018, 7, 26, 15, 59, 12, 831884),
    'sender_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'contract_address': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
    'refund_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'token_address': '0x53E546387A0d054e7FF127923254c0a679DA6DBf'}

She was waiting for the response from Bob for a day but she did not receive any,
so she decided to refund the money from the blockchain:

### 1. Get a wallet from the newtork

    from clove.network import EthereumTestnet

    >>> alice_eth_testnet_wallet = EthereumTestnet.get_wallet(private_key='aliceprivatekey')
    >>> alice_eth_testnet_wallet.address
    '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'

### 2. Create refund transaction

    >>> from clove.network import EthereumTestnet

    >>> eth_testnet = EthereumTestnet()
    >>> alice_contract = eth_testnet.audit_contract(
        '0x209a08f2faaea4c6871cd4947293fa3fada5835e1f589fa7f0ab875a858104af' // Put your initial transaction address
    )
    >>> alice_contract.show_details()
    {'contract_address': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
    'locktime': datetime.datetime(2018, 7, 26, 15, 59, 12),
    'recipient_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'refund_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'secret_hash': 'f1281d5c4b4b49ac582d5ee5cd43b871309e0b28',
    'transaction_address': '0x209a08f2faaea4c6871cd4947293fa3fada5835e1f589fa7f0ab875a858104af',
    'value': Decimal('1000'),
    'value_text': '1000.000000000000000000 BBT',
    'token_address': '0x53E546387A0d054e7FF127923254c0a679DA6DBf'}

    >>> refund = alice_contract.refund()

Please remember, that initial transaction contract is set to be **valid for 48 hours**. Before that time, you will not be able to refund your transaction.

### 3. Sign and publish refund transaction

    >>> refund.sign('aliceprivatekey')
    >>> refund.publish()
    '0xbf13af6b32a0af2406fdfb23705742d2d1d097742af9bf3946029e8d1f3feba3'

### 4. Voilà! Alice should get her ethereum_testnet coins back. You can check it for example [here](https://kovan.etherscan.io/tx/0xbf13af6b32a0af2406fdfb23705742d2d1d097742af9bf3946029e8d1f3feba3).



### II Participate transaction refund

Bob created and published such participating transaction:

    >>> participate_transaction.show_details()
    {'nonce': 113,
    'gasprice': 1000000000,
    'to': '0x9f7e5402ed0858ea0c5914d44b900a42c89547b8',
    'value': Decimal('0.5'),
    'data': '0xeb8ae1ed000000000000000000000000000000000000000000000000000000005b5adcbc8cebcb1af6fa5fddeb091f61f0af1c49a6de9922000000000000000000000000000000000000000000000000999f348959e611f1e9eab2927c21e88e48e6ef45',
    'v': 28,
    'r': 45709055192944493283238091426882972043846668244047220959455715247392544872489,
    's': 32702391840690720592637798834593583073452964948638155547821984857632864140453,
    'sender': '0xd867f293ba129629a9f9355fa285b8d3711a9092',
    'transaction_address': '0xe1de0d46e5f62f8d17a2b6dbe9ad0f2937b6c513a91e0be71a2841e8da48d602',
    'gas_limit': 66221,
    'transaction': '0xf8d171843b9aca00830102ad949f7e5402ed0858ea0c5914d44b900a42c89547b88806f05b59d3b20000b864eb8ae1ed000000000000000000000000000000000000000000000000000000005b5adcbc8cebcb1af6fa5fddeb091f61f0af1c49a6de9922000000000000000000000000000000000000000000000000999f348959e611f1e9eab2927c21e88e48e6ef451ca0650e688ea34735d0443766a0a824ba8a932bd9876f914eb8d777da6437455829a0484ce5d993a945cd3f8dc339a161694e97ff0be0483face8d83c0a46bfc6fca5',
    'recipient_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45', '
    value_text': '0.500000000000000000 ETH',
    'secret': '',
    'secret_hash': '8cebcb1af6fa5fddeb091f61f0af1c49a6de9922',
    'locktime': datetime.datetime(2018, 7, 27, 8, 50, 4, 937035),
    'sender_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'contract_address': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'refund_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092'}

Alice didn't redeem the transaction, so no secret key was published. Bob needed to get his tokens back.

The process is parallel as in the initial transaction.

### 1. Get a wallet from the newtork

    >>> from clove.network import EthereumTestnet

    >>> bob_eth_testnet_wallet = EthereumTestnet.get_wallet(private_key='bobprivatekey')
    >>> bob_eth_testnet_wallet.address
    '0xd867f293Ba129629a9f9355fa285B8D3711a9092'

### 2. Create refund transaction

    >>> from clove.network import EthereumTestnet

    >>> eth_testnet = EthereumTestnet()
    >>> bob_contract = eth_testnet.audit_contract(
        '0xe1de0d46e5f62f8d17a2b6dbe9ad0f2937b6c513a91e0be71a2841e8da48d602' // Put your participate transaction address
    )
    >>> bob_contract.show_details()
    {'contract_address': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
    'locktime': datetime.datetime(2018, 7, 27, 8, 50, 4),
    'recipient_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
    'refund_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
    'secret_hash': '8cebcb1af6fa5fddeb091f61f0af1c49a6de9922',
    'transaction_address': '0xe1de0d46e5f62f8d17a2b6dbe9ad0f2937b6c513a91e0be71a2841e8da48d602',
    'value': Decimal('0.5'),
    'value_text': '0.500000000000000000 ETH'}


    >>> refund = bob_contract.refund()

Please remember, that participate transaction contract is set to be **valid for 24 hours**. Before that time, you will not be able to refund your transaction.

### 3. Sign and publish refund transaction

    >>> refund.sign('bobprivatekey')
    >>> refund.publish()
    '0x28c10e6d0632fb433f6ca7c7fb84db222e4d2ccac39112c91e911c465f21f863'

### 4. Voilà! Bob should get his tokens coins back. You can check it for example [here](https://kovan.etherscan.io/tx/0x28c10e6d0632fb433f6ca7c7fb84db222e4d2ccac39112c91e911c465f21f863).
