# Atomic swap example

## API keys

### Cryptoid API key

For operations on networks supported by `chainz.cryptoid.info` API a [free API key](https://chainz.cryptoid.info/api.key.dws) is needed. This key has to be setup as an environment variable under the `CRYPTOID_API_KEY` key.

    $ export CRYPTOID_API_KEY=YOUR_API_KEY


### Etherscan API key

For operations on Etherscan API (e.q. `find_redeem_transaction`) a [free API key](https://etherscan.io/myapikey) is needed. This key has to be setup as an environment variable under the `ETHERSCAN_API_KEY` key.

    $ export ETHERSCAN_API_KEY=YOUR_API_KEY


### Infura API key

All the interactions with Ethereum network are done via [infura](https://infura.io/).

    $ export INFURA_TOKEN=YOUR_API_KEY


## Bitcoin based networks

### Assumptions

* Alice has over 0.03 monacoins and wants to buy 0.001 litecoins
* Alice doesn't have a litecoin wallet
* Bob has over 0.001 litecoins and wants to buy around 0.03 monacoin
* Bob has a monacoin wallet

(2018-10-04) Exchange rate: 0.001 litecoins is 0.030 monacoin


### 1. Wallets setup

[**Alice**] has to create a new litecoin wallet

    from clove.network import Litecoin

    ltc_network = Litecoin()

    alice_ltc_wallet = ltc_network.get_new_wallet()

    alice_ltc_wallet.address
    'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb'

[Check address on block explorer](https://chainz.cryptoid.info/ltc/address.dws?LXRAXRgPo84p58746zaBXUFFevCTYBPxgb.htm)

    alice_ltc_wallet.get_private_key()
    # returns private key; The one below is fake, because of obvious security reasons.
    'L15kFZg4MdoX2kqXEeEZMjbbVEdZzt1zL2vU59ynrtEf6GB16B3c'

[**Alice**] has to prepare her monacoin wallet

    from clove.network import Monacoin

    mona_network = Monacoin()

    # Alice provides her private key. The one below is fake, because of obvious security reasons.
    alice_mona_wallet = mona_network.get_wallet(private_key='cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe')

    alice_mona_wallet.address
    'MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP'

[Check address on block explorer](https://insight.electrum-mona.org/insight/address/MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP)

[**Bob**] can use his existing monacoin wallet by passing his private key

    from clove.network import Monacoin

    mona_network = Monacoin()

    # Bob provides his private key. The one below is fake, because of obvious security reasons.
    bob_mona_wallet = mona_network.get_wallet(private_key='cRoFBWMvcLXrLsYFt794NRBEPUgMLf5AmnJ7VQwiEenc34z7zSpK')

    bob_mona_wallet.address
    'MWsDkqHLonS5KfbRnRu3feByD9qkuj44Ye'

[Check address on block explorer](https://insight.electrum-mona.org/insight/address/MWsDkqHLonS5KfbRnRu3feByD9qkuj44Ye)

[**Bob**] has to prepare his litecoin wallet

    from clove.network import Litecoin

    ltc_network = Litecoin()

    # Bob provides his private key. The one below is fake, because of obvious security reasons.
    bob_ltc_wallet = ltc_network.get_wallet(private_key='cTVuBqcjryCdHiCfFxkY5ycNPH2RYNrbmgrTVXBsLKG8xR2My3j2')

    bob_ltc_wallet.address
    'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq'

[Check address on block explorer](https://chainz.cryptoid.info/ltc/address.dws?LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq.htm)


### 2. Communication (b1)

Alice and Bob exchange their wallet addresses.

[**Alice**]'s console input:

    bob_mona_address = 'MWsDkqHLonS5KfbRnRu3feByD9qkuj44Ye'
    bob_ltc_address = 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq'

[**Bob**]'s console input:

    alice_mona_address = 'MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP'
    alice_ltc_address = 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb'


### 3. Alice is initializing an atomic swap transaction using Monacoin

[**Alice**] has to prepare an atomic swap transaction


    initial_transaction = mona_network.atomic_swap(
        sender_address=alice_mona_wallet.address,
        recipient_address=bob_mona_address,
        value=0.030,
    )

    initial_transaction.add_fee_and_sign(alice_mona_wallet)

    initial_transaction.show_details()

    {'contract': '63a61450314a793bf317665ecdc54c2e843bb106aeee158876a914fbed00c1502fded3dfa2524f8672ee013bb3f28f670465bab85bb17576a914a96a92963b7a65ac904875cfa5d535b3115888276888ac',
     'contract_address': 'PHVjh4aEgaY5DucNGT6xoFjLD1LAqo9SMu',
     'contract_transaction': '0100000001d4a61b33e849c8df64a2c839b878437a0ef055887ff0bf4279b8a805a2043b69010000006b483045022100a038a71fc3218c67e64804171b8a311397872fff51c85cbef81170570915946b02202385c01f3c4b06416108b6b856ca4f112e79ed74bc36766df4d994a696a7479401210240917aa65f12d8051abae7e8e98eea3b085a766a2dd7bd7f71c8121304cca2980000000002c0c62d000000000017a91461b1cbc5cd1b50e69e1c895d6cbcc94376c4ab3c87345e1401000000001976a914a96a92963b7a65ac904875cfa5d535b31158882788ac00000000',
     'fee': 0.00017655,
     'fee_per_kb': 0.0007881781818181818,
     'fee_per_kb_text': '0.00078818 MONA / 1 kB',
     'fee_text': '0.00017655 MONA',
     'locktime': datetime.datetime(2018, 10, 6, 13, 36, 37, 851140),
     'recipient_address': 'MWsDkqHLonS5KfbRnRu3feByD9qkuj44Ye',
     'refund_address': 'MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP',
     'secret': 'c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9',
     'secret_hash': '50314a793bf317665ecdc54c2e843bb106aeee15',
     'size': 224,
     'size_text': '224 bytes',
     'transaction_address': 'a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473',
     'transaction_link': 'https://insight.electrum-mona.org/insight/tx/a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473',
     'value': 0.03,
     'value_text': '0.03000000 MONA'}

     initial_transaction.publish()
     'a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473'

We can check if the transaction exists by using the `transaction_link` from `show_details()` or by calling the `mona_network.get_transaction(initial_transaction.address)`.

[Check transaction in block explorer](https://insight.electrum-mona.org/insight/tx/a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473)


### 4. Communication (b2)

[**Alice**] sends her transaction address `a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473` and contract `63a61450314a793bf317665ecdc54c2e843bb106aeee158876a914fbed00c1502fded3dfa2524f8672ee013bb3f28f670465bab85bb17576a914a96a92963b7a65ac904875cfa5d535b3115888276888ac` to Bob, so he can audit the transaction.


### 5. Contract audit (MONA)

[**Bob**] needs to create a contract in a network of coins he wants to receive (i.e. Alice's network), in our case in Monacoin network.
And also at this point Bob should validate if the data returned in the contract are correct.

    alice_contract = mona_network.audit_contract(
        contract='63a61450314a793bf317665ecdc54c2e843bb106aeee158876a914fbed00c1502fded3dfa2524f8672ee013bb3f28f670465bab85bb17576a914a96a92963b7a65ac904875cfa5d535b3115888276888ac',
        transaction_address='a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473',
    )
    alice_contract.show_details()

    {'confirmations': 9,
     'contract_address': 'PHVjh4aEgaY5DucNGT6xoFjLD1LAqo9SMu',
     'locktime': datetime.datetime(2018, 10, 6, 13, 36, 37),
     'recipient_address': 'MWsDkqHLonS5KfbRnRu3feByD9qkuj44Ye',
     'refund_address': 'MPLx6eJS41da9bPsLLkHo35uY6KsHu7dXP',
     'secret_hash': '50314a793bf317665ecdc54c2e843bb106aeee15',
     'transaction_address': 'a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473',
     'transaction_link': 'https://insight.electrum-mona.org/insight/tx/a019e444e331ec843ae2d98b87073884e695dd08be06ba91f335af89dbe45473',
     'value': 0.03,
     'value_text': '0.03000000 MONA'}


### 6. Participation (LTC)

[**Bob**] has to create a parallel transaction from point 3 but in his network (i.e. Litecoin network). We call it  a `participate_transaction`.

    participate_transaction = alice_contract.participate(
        symbol='LTC',
        sender_address=bob_ltc_wallet.address,
        recipient_address=alice_ltc_address,
        value=0.001,
    )

    participate_transaction.add_fee_and_sign(bob_ltc_wallet)

    participate_transaction.show_details()

    {'contract': '63a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
     'contract_address': 'MSRzh2WrJ7o3ceSvCTxsuMk6i69kpWrtwS',
     'contract_transaction': '0100000001741a87828215c8bfeef3cfa70925ce91bca806f4f3dd931092f3b1727692504e000000008b483045022100bbd11530d3ea9cdf7b6385ff9aa884acdc04c8cdc96e182360ef5e69fb270512022054c0c5d2024878324af45b7ca5d81b19099e847976a0bbba2d23741a30f6eab401410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f60000000002a08601000000000017a914cb4731b2c83362dcd05bba45e5f0ab8cd8642e4a876b730200000000001976a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac00000000',
     'fee': 2.146e-05,
     'fee_per_kb': 8.415e-05,
     'fee_per_kb_text': '0.00008415 LTC / 1 kB',
     'fee_text': '0.00002146 LTC',
     'locktime': datetime.datetime(2018, 10, 5, 13, 56, 34, 8070),
     'recipient_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
     'refund_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
     'secret': '',
     'secret_hash': '50314a793bf317665ecdc54c2e843bb106aeee15',
     'size': 256,
     'size_text': '256 bytes',
     'transaction_address': '09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa',
     'transaction_link': 'https://chainz.cryptoid.info/ltc/tx.dws?09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa.htm',
     'value': 0.001,
     'value_text': '0.00100000 LTC'}

    participate_transaction.publish()
    '09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa'

[Check transaction on block explorer](https://chainz.cryptoid.info/ltc/tx.dws?09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa.htm)


### 7. Communication (b3)

[**Bob**] sends his transaction address `09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa` and contract `63a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac` to Alice.


### 8. Contract audit (LTC)

[**Alice**] needs to audit the contract in a network of coins she wants to receive (i.e. Bob's network), in our case on the Litecoin network.
And also at this point Alice should validate if the data returned in the contract are correct

    bob_contract = ltc_network.audit_contract(
        contract='63a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
        transaction_address='09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa'
    )

[**Alice**] can check the details of the contract

    bob_contract.show_details()

    {'confirmations': 1,
     'contract_address': 'MSRzh2WrJ7o3ceSvCTxsuMk6i69kpWrtwS',
     'locktime': datetime.datetime(2018, 10, 5, 13, 56, 34),
     'recipient_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
     'refund_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
     'secret_hash': '50314a793bf317665ecdc54c2e843bb106aeee15',
     'transaction_address': '09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa',
     'transaction_link': 'https://chainz.cryptoid.info/ltc/tx.dws?09a60dc3fafe6ba058b2a140457df1c3b446602595d47deed641cb635ffd25aa.htm',
     'value': 0.001,
     'value_text': '0.00100000 LTC'}


### 9. First redeem transaction (LTC)

[**Alice**] can now collect coins she wants, thus she creates redeem transaction.

    alice_redeem = bob_contract.redeem(secret=initial_transaction.show_details()['secret'], wallet=alice_ltc_wallet)
    alice_redeem.add_fee_and_sign()

    alice_redeem.show_details()

    {'fee': 2.886e-05,
     'fee_per_kb': 8.415e-05,
     'fee_per_kb_text': '0.00008415 LTC / 1 kB',
     'fee_text': '0.00002886 LTC',
     'recipient_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
     'size': 342,
     'size_text': '342 bytes',
     'transaction': '0100000001aa25fd5f63cb41d6ee7dd495256046b4c3f17d4540a1b258a06bfefac30da60900000000fdff0047304402201c8869d359b5599ecffd51a96f0a8799392c98c4e15242762ba455e37b1f5d6302203f2974e9afc8d641f9363167df48e5a845a8deba1381bf5a1b549ac04718a1ac01410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf420c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9514c5163a61450314a793bf317665ecdc54c2e843bb106aeee158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e66704926db75bb17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac00000000015a7b0100000000001976a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac00000000',
     'transaction_address': 'a5c027027c695f403fe570850e35ffd44bb28479ecaaee039372015fe0aae7b2',
     'transaction_link': 'https://chainz.cryptoid.info/ltc/tx.dws?a5c027027c695f403fe570850e35ffd44bb28479ecaaee039372015fe0aae7b2.htm',
     'value': 0.001,
     'value_text': '0.00100000 LTC'}

    alice_redeem.publish()
    'a5c027027c695f403fe570850e35ffd44bb28479ecaaee039372015fe0aae7b2'

[Check transaction in block explorer](https://chainz.cryptoid.info/ltc/tx.dws?a5c027027c695f403fe570850e35ffd44bb28479ecaaee039372015fe0aae7b2.htm)

[**Alice**] should get litecoins just after redeem transaction is published.


### 10. Secret capture (LTC)

[**Bob**] should check if his contract has been already redeemed to be able to extract the secret from the redeem transaction.

    contract_address = participate_transaction.show_details()['contract_address']
    secret = ltc_network.extract_secret_from_redeem_transaction(contract_address)
    secret
    'c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9'


### 11. Second redeem transaction (MONA)

[**Bob**] can now collect coins he wants, thus he creates redeem transaction.

    bob_redeem = alice_contract.redeem(secret=secret, wallet=bob_mona_wallet)

    bob_redeem.add_fee_and_sign()

    bob_redeem.show_details()
    {'fee': 0.00014787,
     'fee_per_kb': 0.0004801077777777778,
     'fee_per_kb_text': '0.00048011 MONA / 1 kB',
     'fee_text': '0.00014787 MONA',
     'recipient_address': 'MWsDkqHLonS5KfbRnRu3feByD9qkuj44Ye',
     'size': 309,
     'size_text': '309 bytes',
     'transaction': '01000000017354e4db89af35f391ba06be08dd95e6843807878bd9e23a84ec31e344e419a000000000e0483045022100d3e8f684e2bcdfe43a3f8ea6f6f77a97c7ebfe5e6ba3f280a078f18967d2b43a02204b40068e347e607438c893b83439099bf150f962a5b1009709d513732b4c6f0e0121028164de7b41f30fafac11350539035b38304def75c448d24178b6bc9ac902e95e20c480afb333623864901c968022a07dd93fe3c06f5684ea728b8113e17fa91bd9514c5163a61450314a793bf317665ecdc54c2e843bb106aeee158876a914fbed00c1502fded3dfa2524f8672ee013bb3f28f670465bab85bb17576a914a96a92963b7a65ac904875cfa5d535b3115888276888ac0000000001fd8c2d00000000001976a914fbed00c1502fded3dfa2524f8672ee013bb3f28f88ac00000000',
     'transaction_address': '5d6972cbb7ec034003e7880302d69b2d83b54eb89193a606ff26d7fbb253bba1',
     'transaction_link': 'https://insight.electrum-mona.org/insight/tx/5d6972cbb7ec034003e7880302d69b2d83b54eb89193a606ff26d7fbb253bba1',
     'value': 0.03,
     'value_text': '0.03000000 MONA'}

    bob_redeem.publish()
    '5d6972cbb7ec034003e7880302d69b2d83b54eb89193a606ff26d7fbb253bba1'


[Check transaction in block explorer](https://insight.electrum-mona.org/insight/tx/5d6972cbb7ec034003e7880302d69b2d83b54eb89193a606ff26d7fbb253bba1)

[**Bob**] should get monacoins just after redeem transaction is published.



## Ethereum Testnet


### Assumptions

* Alice wants to buy 0.5 ETH for 1000 Blockbusters Test tokens in Ethereum Kovan Testnet
* Bob wants to buy 1000 Blockbusters Test tokens for 0.5 ETH in Ethereum Kovan Testnet
* Both Alice and Bob have wallets in Ethereum Kovan network


### 1. Setup

Alice should initialize the network object, set her address, private key, amount of tokens to be swapped and the address of the token.

[**Alice**]'s console input:

    from clove.network import EthereumTestnet
    eth_test = EthereumTestnet()

    address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'
    private_key = 'alice_private_key'

    tokens_to_swap = '1000'
    token_address = '0x53E546387A0d054e7FF127923254c0a679DA6DBf'

It is also possible to get the token data directly from the network object by the token symbol if the token is supported:

    token = eth_test.get_token_by_symbol('BBT')
    token_address = token.token_address

Bob should initialize the network object, set his address, private key and amount of ethers to be swapped.

[**Bob**]'s console input:

    from clove.network import EthereumTestnet
    eth_test = EthereumTestnet()

    address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'
    private_key = 'bob_private_key'

    eth_to_swap = '0.5'


### 2. Communication (e1)

Alice and Bob exchange their wallet addresses.

[**Alice**]'s console input:

    bob_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'

[**Bob**]'s console input:

    alice_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'


### 3. Token approval

To send tokens to an atomic swap contract Alice has to first approve that the tokens she owns can be spent by that contract.

    approve_transaction = eth_test.approve_token(address, tokens_to_swap, token_address)
    approve_transaction.sign(private_key)
    approve_transaction.show_details()

    {'contract_address': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
     'data': '0x095ea7b30000000000000000000000007657ca877fac31d20528b473162e39b6e152fd2e00000000000000000000000000000000000000000000003635c9adc5dea00000',
     'gasprice': 20000000000,
     'nonce': 34,
     'r': 112426775415197512764524506063660144184257199595961926193168166347175765778579,
     's': 1927313746114385663128009448899947006587692267799486537632890580735710981604,
     'sender': '0x999f348959e611f1e9eab2927c21e88e48e6ef45',
     'sender_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
     'startgas': 45576,
     'token_address': '0x53E546387A0d054e7FF127923254c0a679DA6DBf',
     'transaction_address': '0x40b8d435ff4bfbb202aed75dfc87f64e0d3da3838581b6635ae615e0454bd4fc',
     'v': 28,
     'value': Decimal('1000'),
     'value_text': '1000.000000000000000000 BBT'}

    approve_transaction.publish()
    '0x40b8d435ff4bfbb202aed75dfc87f64e0d3da3838581b6635ae615e0454bd4fc'

[Check transaction on block explorer](https://kovan.etherscan.io/tx/0x40b8d435ff4bfbb202aed75dfc87f64e0d3da3838581b6635ae615e0454bd4fc)


### 4. Alice is initializing an atomic swap transaction using BBT token

    initial_transaction = eth_test.atomic_swap(
        sender_address=address,
        recipient_address=bob_address,
        value=tokens_to_swap,
        token_address=token_address
    )
    initial_transaction.sign(private_key)
    initial_transaction.show_details()

    {'contract_address': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
     'data': '0x52f50db7000000000000000000000000000000000000000000000000000000005acde5c48cebcb1af6fa5fddeb091f61f0af1c49a6de9922000000000000000000000000000000000000000000000000d867f293ba129629a9f9355fa285b8d3711a909200000000000000000000000053e546387a0d054e7ff127923254c0a679da6dbf00000000000000000000000000000000000000000000003635c9adc5dea00000',
     'gas_limit': None,
     'gasprice': 20000000000,
     'locktime': datetime.datetime(2018, 4, 11, 10, 39, 0, 535753),
     'nonce': 35,
     'r': 81080759208730988867907650750974367955166566527430658028938499115001735694910,
     'recipient_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
     'refund_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
     's': 25371208205154004938960599477560107420234164093623357637201902103097079815422,
     'secret': 'c037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac',
     'secret_hash': '8cebcb1af6fa5fddeb091f61f0af1c49a6de9922',
     'sender': '0x999f348959e611f1e9eab2927c21e88e48e6ef45',
     'sender_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
     'startgas': 300000,
     'to': '0x7657ca877fac31d20528b473162e39b6e152fd2e',
     'token_address': '0x53E546387A0d054e7FF127923254c0a679DA6DBf',
     'transaction_address': '0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840',
     'v': 27,
     'value': Decimal('1000'),
     'value_text': '1000.000000000000000000 BBT'}

    initial_transaction.publish()
    '0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840'

[Check transaction on block explorer](https://kovan.etherscan.io/tx/0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840)


### 5. Communication (e2)

[**Alice**] sends her transaction address `0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840` to Bob so he can audit created contract.


### 6. Contract audit (BBT token)

[**Bob**] needs to audit the contract in the network it was created in, in our case it's Ethereum Testnet network.
And also at this point Bob should validate if the data returned in the contract are correct.

    alice_contract = eth_test.audit_contract('0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840')
    alice_contract.show_details()

    {'contract_address': '0x7657Ca877Fac31D20528B473162E39B6E152fd2e',
     'locktime': datetime.datetime(2018, 4, 11, 10, 39),
     'recipient_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
     'refund_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
     'secret_hash': '8cebcb1af6fa5fddeb091f61f0af1c49a6de9922',
     'token_address': '0x53E546387A0d054e7FF127923254c0a679DA6DBf',
     'transaction_address': '0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840',
     'value': Decimal('1000'),
     'value_text': '1000.000000000000000000 BBT'}


### 7. Participation (ETH-TESTNET)

[**Bob**] has to create a parallel transaction from point 4 but for 0.5 ETH. We call it `participate_transaction`.

    participate_transaction = alice_contract.participate(
        symbol='ETH-TESTNET',
        sender_address=address,
        recipient_address=alice_address,
        value=eth_to_swap
    )

    participate_transaction.sign(private_key)
    participate_transaction.show_details()

    {'contract_address': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
     'data': '0xeb8ae1ed000000000000000000000000000000000000000000000000000000005acca1d68cebcb1af6fa5fddeb091f61f0af1c49a6de9922000000000000000000000000000000000000000000000000999f348959e611f1e9eab2927c21e88e48e6ef45',
     'gas_limit': 126221,
     'gasprice': 20000000000,
     'locktime': datetime.datetime(2018, 4, 10, 11, 36, 54, 224171),
     'nonce': 18,
     'r': 10117394961799586109544014237169747431096329877057063230289022533801441532789,
     'recipient_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
     'refund_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
     's': 34556783084242874049490624129921763496945955547455400337813271950949674389178,
     'secret_hash': '8cebcb1af6fa5fddeb091f61f0af1c49a6de9922',
     'sender': '0xd867f293ba129629a9f9355fa285b8d3711a9092',
     'sender_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
     'startgas': 126221,
     'to': '0x9f7e5402ed0858ea0c5914d44b900a42c89547b8',
     'transaction_address': '0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f',
     'v': 28,
     'value': Decimal('0.5'),
     'value_text': '0.500000000000000000 ETH'}

    participate_transaction.publish()
    '0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f'

[Check transaction on block explorer](https://kovan.etherscan.io/tx/0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f)

### 8. Communication (e3)

[**Bob**] sends his transaction address `0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f` to Alice.


### 9. Contract audit (ETH-TESTNET)

[**Alice**] needs to audit the contract in the network it was created in, in our case it's Ethereum Testnet network.
And also at this point Alice should validate if the data returned in the contract are correct.

    bob_contract = eth_test.audit_contract(
        '0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f'
    )
    bob_contract.show_details()

    {'contract_address': '0x9F7e5402ed0858Ea0C5914D44B900A42C89547B8',
     'locktime': datetime.datetime(2018, 4, 10, 11, 36, 54),
     'recipient_address': '0x999F348959E611F1E9eab2927c21E88E48e6Ef45',
     'refund_address': '0xd867f293Ba129629a9f9355fa285B8D3711a9092',
     'secret_hash': '8cebcb1af6fa5fddeb091f61f0af1c49a6de9922',
     'transaction_address': '0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f',
     'value': Decimal('0.5'),
     'value_text': '0.500000000000000000 ETH'}


### 10. First redeem transaction (ETH-TESTNET)

[**Alice**] can now collect coins she wants, thus she creates redeem transaction.

    alice_redeem = bob_contract.redeem(secret=initial_transaction.show_details()['secret'])
    alice_redeem.sign(private_key)

    alice_redeem.show_details()

    {'data': '0xeda1122cc037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac',
     'gasprice': 20000000000,
     'hash': '0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1',
     'nonce': 36,
     'r': 59319998726546023363151651169655572196637192178004534224886682741537229136353,
     's': 49667378228500740364784037188336222900603288337407062594007817473604371090679,
     'sender': '0x999f348959e611f1e9eab2927c21e88e48e6ef45',
     'startgas': 100000,
     'to': '0x9f7e5402ed0858ea0c5914d44b900a42c89547b8',
     'v': 28,
     'value': Decimal('0.5'),
     'value_text': '0.500000000000000000 ETH'}

    alice_redeem.publish()
    '0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1'

[Check transaction on block explorer](https://kovan.etherscan.io/tx/0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1)

[**Alice**] will get ether just after redeem transaction is published.


### 11. Secret capture (ETH-TESTNET)

[**Bob**] should extract the secret from the redeem transaction. For this operation (`find_redeem_transaction`) an Etherscan API key is required - [read more](#etherscan-api-key)

    alice_redeem_tx_hash = participate_transaction.find_redeem_transaction()
    secret = eth_test.extract_secret_from_redeem_transaction(alice_redeem_tx_hash)
    secret
    'c037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac'


### 12. Second redeem transaction (BBT token)

[**Bob**] can now collect tokens he wants, thus he creates redeem transaction.

    bob_redeem = alice_contract.redeem(secret)
    bob_redeem.sign(private_key)

    bob_redeem.show_details()

    {'data': '0xeda1122cc037026e2d0f3901c797d2414df30a4ce700d18055925f416e575635c5c2b7ac',
     'gasprice': 20000000000,
     'hash': '0x4fd41289b816f6122e59a0759bd10441ead75d550562f4b3aad2fddc56eb3274',
     'nonce': 19,
     'r': 65751206609566246138168255228214505208801025362644939199208252280848271690158,
     's': 45667062183625152271430540771543035424773489029161348648874675951038677865195,
     'sender': '0xd867f293ba129629a9f9355fa285b8d3711a9092',
     'startgas': 100000,
     'to': '0x7657ca877fac31d20528b473162e39b6e152fd2e',
     'v': 27,
     'value': Decimal('1000'),
     'value_text': '1000.000000000000000000 BBT'}

    bob_redeem.publish()
    '0x4fd41289b816f6122e59a0759bd10441ead75d550562f4b3aad2fddc56eb3274'

[Check transaction on block explorer](https://kovan.etherscan.io/tx/0x4fd41289b816f6122e59a0759bd10441ead75d550562f4b3aad2fddc56eb3274)


[**Bob**] will get BBT tokens just after redeem transaction is published.
