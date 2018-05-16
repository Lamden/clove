# Clove atomic swap example

* [Bitcoin based networks](#bitcoin-based-networks)
* [Ethereum Testnet](#ethereum-testnet)

# Bitcoin based networks

## Assumptions

* Alice has over 0.4 monacoins and wants to buy 0.01 litecoins
* Alice doesn't have a litecoin wallet
* Bob has over 0.01 litecoins and wants to buy around 0.4 monacoin
* Bob has a monacoin wallet

(2018-03-01) Exchange rate: 0.01 litecoins is 0.4 monacoin


### Cryptoid API key

For operations on networks supported by `chainz.cryptoid.info` API a [free API key](https://chainz.cryptoid.info/api.key.dws) is needed. This key has to be setup as a environment variable under the `CRYPTOID_API_KEY` key.

    $ export CRYPTOID_API_KEY=YOUR_API_KEY


### Etherscan API key

For operations on Etherscan API (e.q. `find_redeem_transaction`) a [free API key](https://etherscan.io/myapikey) is needed. This key has to be setup as a environment variable under the `ETHERSCAN_API_KEY` key.

    $ export ETHERSCAN_API_KEY=YOUR_API_KEY


## 1. Wallets setup

[**Alice**] has to create a new litecoin wallet

    from clove.network import Litecoin

    ltc_network = Litecoin()

    alice_ltc_wallet = ltc_network.get_new_wallet()

    alice_ltc_wallet.address
    'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb'
https://live.blockcypher.com/ltc/address/LXRAXRgPo84p58746zaBXUFFevCTYBPxgb/

    alice_ltc_wallet.get_private_key()
    # returns private key; The one below is fake, because of obvious security reasons.
    'L15kFZg4MdoX2kqXEeEZMjbbVEdZzt1zL2vU59ynrtEf6GB16B3c'

[**Alice**] has to prepare her monacoin wallet

    from clove.network import Monacoin

    mona_network = Monacoin()

    # Alice provides hers private key. The one below is fake, because of obvious security reasons.
    alice_mona_wallet = mona_network.get_wallet(private_key='cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe')

    alice_mona_wallet.address
    'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ'
https://bchain.info/MONA/addr/MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ

[**Bob**] can use his existing monacoin wallet by passing his private key

    from clove.network import Monacoin

    mona_network = Monacoin()

    bob_mona_wallet = mona_network.get_wallet(private_key='cRoFBWMvcLXrLsYFt794NRBEPUgMLf5AmnJ7VQwiEenc34z7zSpK')

    bob_mona_wallet.address
    'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL'
https://bchain.info/MONA/addr/MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL

[**Bob**] has to prepare his litecoin wallet

    from clove.network import Litecoin

    ltc_network = Litecoin()

    # Bob provides his private key. The one below is fake, because of obvious security reasons.
    bob_ltc_wallet = ltc_network.get_wallet(private_key='cTVuBqcjryCdHiCfFxkY5ycNPH2RYNrbmgrTVXBsLKG8xR2My3j2')

    bob_ltc_wallet.address
    'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq'
https://live.blockcypher.com/ltc/address/LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq/

## 2. Communication

Alice and Bob exchange their wallet addresses.

[**Alice**]'s console input:

    bob_mona_address = 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL'
    bob_ltc_address = 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq'

[**Bob**]'s console input:

    alice_mona_address = 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ'
    alice_ltc_address = 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb'


## 3. Alice is initializing an atomic swap transaction

[**Alice**] has to prepare a transaction input (UTXO's that she wants to spend in this transaction). You can find this information by viewing transaction on block explorer e.g. [here](https://bchain.info/MONA/tx/5a82da68900bb725f1ac7e2a8f51a41dea12873c99c2d28a32942e04395323fd)

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs UTXOs can also be gathered automatically.
See an exmaple in [Participation](#6-participation). For `chainz.cryptoid.info`, an API key is required - [read more](#cryptoid-api-key).

    from clove.network.bitcoin.utxo import Utxo

    monacoins_to_swap = 0.4

    initial_utxo_list = [
        Utxo(
            tx_id='5d920e7093b2f0ac94cb1c13a42a79ed1c1290fcc4155d15a123d69b1afe05d2',
            vout=1,
            value=2.086,
            tx_script='76a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac'
        ),
    ]

    initial_transaction = mona_network.atomic_swap(
        alice_mona_wallet.address,
        bob_mona_address,
        monacoins_to_swap,
        initial_utxo_list
    )

    # As monacoin is not in the blockcypher we need to add fee manually
    initial_transaction.fee = 0.001

    initial_transaction.add_fee_and_sign(alice_mona_wallet)

    initial_transaction.show_details()

    {'contract': '63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac',
     'contract_address': '3QNHtUAJ85WWfF1rXPpLde4CjwYKcJYLiv',
     'contract_transaction': '0100000001d205fe1a9bd623a1155d15c4fc90121ced792aa4131ccb94acf0b293700e925d010000008a473044022003d3f4216fdc08be20c2d828227d8652e89dcf20566719a561265d3886c0fda7022035fb05dd2bc1b9e325837af29b0e7687815e5544f643a24480aa09ddfc10cb460141044fbe9cf6ef9bf4a13a693ee1d431eb700a592e8097619e0cfe82aff2a5c231e7154e464e4ec94201007b403b6de9a5819b0bc31eef0741c4fe6e932bca6d9cca0000000002005a62020000000017a914f8c050e6c124b3d0b693779b418dec5f40b8188087201b0b0a000000001976a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac00000000',
     'fee': 0.001,
     'fee_per_kb': 0.0,
     'fee_per_kb_text': '0.00000000 MONA / 1 kB',
     'fee_text': '0.00100000 MONA',
     'locktime': datetime.datetime(2018, 4, 22, 11, 3, 11, 86941),
     'recipient_address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
     'refund_address': 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ',
     'secret': '9a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2',
     'secret_hash': '98ff8f419c57646b3e056514185a97d15a7f086e',
     'size': 255,
     'size_text': '255 bytes',
     'transaction_address': 'a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4',
     'value': 0.4,
     'value_text': '0.40000000 MONA'}

     initial_transaction.publish()
     'a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4'
https://bchain.info/MONA/tx/a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4


## 4. Communication

[**Alice**] sends her transaction hash `a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4` to Bob, so he can get the `raw_transaction` (e.g. "hex" in raw data of [transaction](https://bchain.info/MONA/tx/a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4)).
And also she needs to send the contract to Bob (i.e. `63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac`)


## 5. Contract audit

[**Bob**] needs to create a contract in network of coins he wants to receive (i.e. Alice's network), in our case in Monacoin network.
And also at this point Bob should validate if the data returned in the contract is correct. He should also check if the transaction is present in the blockchain API (e.g. Bchain.info)

    alice_contract = mona_network.audit_contract(
        contract='63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac',
        raw_transaction='0100000001d205fe1a9bd623a1155d15c4fc90121ced792aa4131ccb94acf0b293700e925d010000008a473044022003d3f4216fdc08be20c2d828227d8652e89dcf20566719a561265d3886c0fda7022035fb05dd2bc1b9e325837af29b0e7687815e5544f643a24480aa09ddfc10cb460141044fbe9cf6ef9bf4a13a693ee1d431eb700a592e8097619e0cfe82aff2a5c231e7154e464e4ec94201007b403b6de9a5819b0bc31eef0741c4fe6e932bca6d9cca0000000002005a62020000000017a914f8c050e6c124b3d0b693779b418dec5f40b8188087201b0b0a000000001976a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac00000000',
    )
    alice_contract.show_details()

    {'contract_address': '3QNHtUAJ85WWfF1rXPpLde4CjwYKcJYLiv',
     'locktime': datetime.datetime(2018, 4, 22, 11, 3, 11),
     'recipient_address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
     'refund_address': 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ',
     'secret_hash': '98ff8f419c57646b3e056514185a97d15a7f086e',
     'transaction_address': 'a0110ac963517ea12935fabe92ecd90217ba6847069dad21f9523bbc83bbf0e4',
     'value': 0.4,
     'value_text': '0.40000000 MONA'}


## 6. Participation

[**Bob**] has to create a parallel transaction from point 3 but in his network (i.e. Litecoin network). We call it  a `participate_transaction`.

    from clove.network.bitcoin.utxo import Utxo
    from clove.utils.bitcoin import from_base_units # blockcypher is showing value in satoshis

    litecoins_to_swap = 0.01
    participate_utxo_list = [
        Utxo(
            tx_id='42394cedfaeecdbfce788ea3291784177f4f28c83f038adca3864db0c48869ab',
            vout=1,
            value=from_base_units(2437887),
            tx_script='76a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac',
        ),
    ]

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs the UTXOs can also be gathered automatically. For `chainz.cryptoid.info`, an API key is required - [read more](#cryptoid-api-key).

    participate_utxo_list = ltc_network.get_utxo(bob_ltc_wallet.address, litecoins_to_swap)

With the list of UTXOs `participate_transaction` can be created.

    participate_transaction = alice_contract.participate(
        'ltc',
        bob_ltc_wallet.address,
        alice_ltc_address,
        litecoins_to_swap,
        participate_utxo_list
    )

    participate_transaction.add_fee_and_sign(bob_ltc_wallet)

    participate_transaction.show_details()

    {'contract': '63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
     'contract_address': 'MWXzG4RaH4VH6hiNKakxkZQqW7NSHYRGrA',
     'contract_transaction': '0100000002be1c074d0e9e119b2099aa792ebda8c0c4a432a22c79490634a556da38435f67000000008a4730440220042d58c03f0db46727770a4c81543ee90294b87ea606baa2ff589d2dd5857c5c02206c5a8ea6e6579191ed3485523a8b27d28db666205c2a2d8477764cc6c6b913e801410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f600000000e930c516c102222acd2439a5b4fe462188c56e8e236588c53a689e2dbf86b6dd010000008a473044022043154c8c7935bff74743551863169fe8617a4c1043894786b4a7d14c46f68905022040431412a306ca13d4bd791ae3cd07e9e6eaa6982d105b07d0cd52a05fc7b1fd01410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f6000000000240420f000000000017a914f849d56da5d65cc96764c25fbcd79161f170f67a872e590400000000001976a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac00000000',
     'fee': 0.00030225,
     'fee_per_kb': 0.00069482,
     'fee_per_kb_text': '0.00069482 LTC / 1 kB',
     'fee_text': '0.00030225 LTC',
     'locktime': datetime.datetime(2018, 4, 21, 11, 41, 17, 629962),
     'recipient_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
     'refund_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
     'secret': '',
     'secret_hash': '98ff8f419c57646b3e056514185a97d15a7f086e',
     'size': 434,
     'size_text': '434 bytes',
     'transaction_address': '565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50',
     'value': 0.01,
     'value_text': '0.01000000 LTC'}

    participate_transaction.publish()
    '565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50'
https://live.blockcypher.com/ltc/tx/565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50/

## 7. Communication

[**Bob**] sends his transaction hash `565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50` and contract `63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac` to Alice.


## 8. Contract audit

[**Alice**] needs to audit the contract in network of coins she wants to receive (i.e. Bob's network), in our case on the Litecoin network.
And also at this point Alice should validate if the data returned in the contract is correct. She should also check if the transaction is present in the blockchain API (e.g. Blockexplorer)

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs contract audit can be done based on contract and transaction hash.
    bob_contract = ltc_network.audit_contract(
        contract='63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
        transaction_address='565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50'
    )

For unsupported networks Alice should find the raw transaction for given transaction address by herself.
    bob_contract = ltc_network.audit_contract(
        contract='63a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac',
        raw_transaction='0100000002be1c074d0e9e119b2099aa792ebda8c0c4a432a22c79490634a556da38435f67000000008a4730440220042d58c03f0db46727770a4c81543ee90294b87ea606baa2ff589d2dd5857c5c02206c5a8ea6e6579191ed3485523a8b27d28db666205c2a2d8477764cc6c6b913e801410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f600000000e930c516c102222acd2439a5b4fe462188c56e8e236588c53a689e2dbf86b6dd010000008a473044022043154c8c7935bff74743551863169fe8617a4c1043894786b4a7d14c46f68905022040431412a306ca13d4bd791ae3cd07e9e6eaa6982d105b07d0cd52a05fc7b1fd01410431ab07973bbb5dbc6b7422fc7322abb5df15f77694c0b15b09a325996af47ddd887c7eaa72c656a71fcb333068956de7b3e2f15deaafc1d9285d779ca1b6a3f6000000000240420f000000000017a914f849d56da5d65cc96764c25fbcd79161f170f67a872e590400000000001976a914621f617c765c3caa5ce1bb67f6a3e51382b8da2988ac00000000'
    )


    bob_contract.show_details()

    {'contract_address': 'MWXzG4RaH4VH6hiNKakxkZQqW7NSHYRGrA',
     'locktime': datetime.datetime(2018, 4, 21, 11, 41, 17),
     'recipient_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
     'refund_address': 'LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq',
     'secret_hash': '98ff8f419c57646b3e056514185a97d15a7f086e',
     'transaction_address': '565c1a6d3e533760e454fe1b7b55a63fafb2438cde4e285f1415b34f5aab5c50',
     'value': 0.01,
     'value_text': '0.01000000 LTC'}


## 9. First redeem transaction

[**Alice**] can now collect coins she wants, thus she creates redeem transaction.

    alice_redeem = bob_contract.redeem(secret=initial_transaction.show_details()['secret'], wallet=alice_ltc_wallet)
    alice_redeem.add_fee_and_sign()

    alice_redeem.show_details()

    {'fee': 0.00023832,
     'fee_per_kb': 0.00069482,
     'fee_per_kb_text': '0.00069482 LTC / 1 kB',
     'fee_text': '0.00023832 LTC',
     'recipient_address': 'LXRAXRgPo84p58746zaBXUFFevCTYBPxgb',
     'size': 343,
     'size_text': '343 bytes',
     'transaction': '0100000001505cab5a4fb315145f284ede8c43b2af3fa6557b1bfe54e46037533e6d1a5c5600000000fd0001483045022100d63353332b762551f3278ea02ab25746ddc78aae08c73cfd81e7871b54ebee88022068fa0e3b6578efbfed07373b2147b190ebe6466d2cdbed15cc2eecb0f218837001410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4209a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac000000000128e50e00000000001976a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac00000000',
     'transaction_address': '0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec',
     'value': 0.01,
     'value_text': '0.01000000 LTC'}

    alice_redeem.publish()
    '0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec'
https://live.blockcypher.com/ltc/tx/0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec/

[**Alice**] should get litecoins just after redeem transaction is published.


## 10. Secret capture

[**Bob**] should check if his contract has been already redeemed to be able to extract the secret from the redeem transaction.

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs this can be done automatically.

    contract_address = participate_transaction.show_details()['contract_address']
    secret = ltc_network.extract_secret_from_redeem_transaction(contract_address)

For `chainz.cryptoid.info` API key is required - [read more](#cryptoid-api-key).

For unsupported networks Bob should extract the secret himself.
First by using the `contract_address` he need to find [the contract](https://chainz.cryptoid.info/ltc/address.dws?MLPZyHgX3dFEWFXTcUpsjBU1p3QsXfUFJ7.htm) and the last transacion there (first from the top) will be the [redeem transaction](https://api.blockcypher.com/v1/ltc/main/txs/25e3b32de672c1f287424a0a9ef23984f5132fc184b182d25476795761925ad2?limit=50&includeHex=true).

by using `hex` field (whole transaction)

    secret = ltc_network.extract_secret(raw_transaction='0100000001505cab5a4fb315145f284ede8c43b2af3fa6557b1bfe54e46037533e6d1a5c5600000000fd0001483045022100d63353332b762551f3278ea02ab25746ddc78aae08c73cfd81e7871b54ebee88022068fa0e3b6578efbfed07373b2147b190ebe6466d2cdbed15cc2eecb0f218837001410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4209a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac000000000128e50e00000000001976a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac00000000')

or `script` field from the first input:

    secret = ltc_network.extract_secret(scriptsig='483045022100d63353332b762551f3278ea02ab25746ddc78aae08c73cfd81e7871b54ebee88022068fa0e3b6578efbfed07373b2147b190ebe6466d2cdbed15cc2eecb0f218837001410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4209a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57646b3e056514185a97d15a7f086e8876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045d23db5ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac')

## 11. Second redeem transaction

[**Bob**] can now collect coins he wants, thus he creates redeem transaction.

    bob_redeem = alice_contract.redeem(secret=secret, wallet=bob_mona_wallet)

    # As monacoin is not in the blockcypher we need to add fee manually
    bob_redeem.fee = 0.001
    bob_redeem.add_fee_and_sign()

    bob_redeem.show_details()
    {'fee': 0.001,
     'fee_per_kb': 0.0,
     'fee_per_kb_text': '0.00000000 MONA / 1 kB',
     'fee_text': '0.00100000 MONA',
     'recipient_address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
     'size': 343,
     'size_text': '343 bytes',
     'transaction': '0100000001e4f0bb83bc3b52f921ad9d064768ba1702d9ec92befa3529a17e5163c90a11a000000000fd0001483045022100bf0dec5ab03d024147bc26df33a64f2389c4647fc1f9a92e93575cb5f2ff5081022060a54dd5135bc38eb6e75c65ec4e47efa08e7298fed83757db31bd53619a17d501410447408e366d0e979101f776ab10753091b0b62ba9aa609d006263959e030fb2d96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1abb209a2cfc32611dbd3ac3261cd23622223e85e6c6575852d20e031c1333b9070bc2514c5163a61498ff8f419c57646b3e056514185a97d15a7f086e8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704ef6bdc5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac000000000160d36002000000001976a9141a376f6634e41c22b28bc9ef3336a623717083a488ac00000000',
     'transaction_address': '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697',
     'value': 0.4,
     'value_text': '0.40000000 MONA'}

    bob_redeem.publish()
    '1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697'
https://bchain.info/MONA/tx/1593f8ac14340e23d629342881e188b848af3dc1b7909791aacde53d48a1e697


[**Bob**] should get monacoins just after redeem transaction is published.

# Ethereum Testnet

## Assumptions

* Alice wants to buy 0.5 ETH for 1000 Blockbusters Test tokens in Ethereum Kovan Testnet
* Bob wants to buy 1000 Blockbusters Test tokens for 0.5 ETH in Ethereum Kovan Testnet
* Both Alice and Bob have wallets in Ethereum Kovan network

## 1. Setup

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

## 2. Communication

Alice and Bob exchange their wallet addresses.

[**Alice**]'s console input:

    bob_address = '0xd867f293Ba129629a9f9355fa285B8D3711a9092'

[**Bob**]'s console input:

    alice_address = '0x999F348959E611F1E9eab2927c21E88E48e6Ef45'

## 3. Token approval

To send tokens to an atomic swap contract Alice has to first approve that the tokens she own can be spend by that contract.

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
https://kovan.etherscan.io/tx/0x40b8d435ff4bfbb202aed75dfc87f64e0d3da3838581b6635ae615e0454bd4fc


## 4. Alice is initializing an atomic swap transaction

    initial_transaction = eth_test.atomic_swap(
        address,
        bob_address,
        tokens_to_swap,
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
https://kovan.etherscan.io/tx/0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840

## 5. Communication

[**Alice**] sends hers transaction address `0x4cc2308652423a1b05712def62fe5183dfa507bd033941bdb40b56a258760840` to Bob so he can audit created contract.


## 6. Contract audit

[**Bob**] needs to audit the contract in the network it was created in, in our case it's Ethereum Testnet network.
And also at this point Bob should validate if the data returned in the contract is correct.

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


## 7. Participation

[**Bob**] has to create parallel transaction from point 4 but for 0.5 ETH. We call it `participate_transaction`.

    participate_transaction = alice_contract.participate(
        'ETH-TESTNET',
        address,
        alice_address,
        eth_to_swap
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
https://kovan.etherscan.io/tx/0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f

## 8. Communication

[**Bob**] sends his transaction address `0xc9b2bf9b67dcfea39dea71b3416922adfcae23f6410be7d109fb9df2e1c0695f` to Alice.


## 9. Contract audit

[**Alice**] needs to audit the contract in the network it was created in, in our case it's Ethereum Testnet network.
And also at this point Alice should validate if the data returned in the contract is correct.

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


## 10. First redeem transaction

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
https://kovan.etherscan.io/tx/0x80addbc1b1ff0cf32949c78cde0dc4347f1a81e7f510fd266aa934523c92c2c1

[**Alice**] will get ether just after redeem transaction is published.


## 11. Secret capture

[**Bob**] should extract the secret from the redeem transaction. For this operation (`find_redeem_transaction`) an Etherscan API key is required - [read more](#etherscan-api-key)

    alice_redeem_tx_hash = bob_contract.find_redeem_transaction()
    secret = eth_test.extract_secret_from_redeem_transaction(alice_redeem_tx_hash)

## 12. Second redeem transaction

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
https://kovan.etherscan.io/tx/0x4fd41289b816f6122e59a0759bd10441ead75d550562f4b3aad2fddc56eb3274


[**Bob**] will get BBT tokens just after redeem transaction is published.
