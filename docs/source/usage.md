# Clove atomic swap example


## Assumptions

* Alice has over 2 monacoins and wants to buy 100 dogecoins
* Alice doesn't have a dogecoin wallet
* Bob has over 1000 dogecoins and wants to buy around 0.11 monacoin
* Bob has a monacoin wallet

(2018-03-01) Exchange rate: 100 dogecoins is 0.11 monacoin


### Cryptoid API key

For operations on networks supported by `chainz.cryptoid.info` API a [free API key](https://chainz.cryptoid.info/api.key.dws) is needed. This key has to be setup as a environment variable under the `CRYPTOID_API_KEY` key.

    $ export CRYPTOID_API_KEY=YOUR_API_KEY


## 1. Wallets setup

[**Alice**] has to create a new dogecoin wallet

    from clove.network import Dogecoin

    doge_network = Dogecoin()

    alice_doge_wallet = doge_network.get_new_wallet()

    alice_doge_wallet.address
    'DE8tMBC9qk6a9A5T7NSdog4MJa16JqzZf7'
https://live.blockcypher.com/doge/address/DE8tMBC9qk6a9A5T7NSdog4MJa16JqzZf7/

    alice_doge_wallet.get_private_key()
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

[**Bob**] has to prepare his dogecoin wallet

    from clove.network import Dogecoin

    doge_network = Dogecoin()

    # Bob provides his private key. The one below is fake, because of obvious security reasons.
    bob_doge_wallet = doge_network.get_wallet(private_key='cTVuBqcjryCdHiCfFxkY5ycNPH2RYNrbmgrTVXBsLKG8xR2My3j2')

    bob_doge_wallet.address
    'DGC1MHWRaQeqn6MTeqkphzUHTeDnZgLvqs'
https://live.blockcypher.com/doge/address/DGC1MHWRaQeqn6MTeqkphzUHTeDnZgLvqs/

## 2. Communication

Alice and Bob exchange their wallet addresses.

[**Alice**]'s console input:

    bob_mona_address = 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL'
    bob_doge_address = 'DGC1MHWRaQeqn6MTeqkphzUHTeDnZgLvqs'

[**Bob**]'s console input:

    alice_mona_address = 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ'
    alice_doge_address = 'DE8tMBC9qk6a9A5T7NSdog4MJa16JqzZf7'


## 3. Alice is initializing an atomic swap transaction

[**Alice**] has to prepare a transaction input (UTXO's that she wants to spend in this transaction). You can find these information by viewing transaction on block explorer e.g. [link](https://bchain.info/MONA/tx/9fcc235b4c1830f6eb1c67be807aeda0a3f7290eb05caf948f4b9f1016c8bffd)

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs UTXOs can also be gathered automatically.
See an exmaple in [Participation](#6-participation). For `chainz.cryptoid.info` API key is required - [read more](#cryptoid-api-key).

    from clove.network.bitcoin.utxo import Utxo

    monacoins_to_swap = 0.11

    initial_utxo_list = [
        Utxo(
            tx_id='9fcc235b4c1830f6eb1c67be807aeda0a3f7290eb05caf948f4b9f1016c8bffd',
            vout=0,
            value=2.8,
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

    {'contract': '63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704b0749a5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac',
     'contract_address': '3HU9muPrDbzm6f3B3pESkwd3gBx6Rafnd6',
     'contract_transaction': '0100000001fdbfc816109f4b8f94af5cb00e29f7a3a0ed7a80be671cebf630184c5b23cc9f000000008b483045022100b8ff6dffca1c42a8879c42dae6be9d65f3ba85e7abe9b8a1aefd526b7a39bbdb02207c5778bddc1d04c2018cc6a14c3be63855a9e130511d5180cab7b4124b1e99930141044fbe9cf6ef9bf4a13a693ee1d431eb700a592e8097619e0cfe82aff2a5c231e7154e464e4ec94201007b403b6de9a5819b0bc31eef0741c4fe6e932bca6d9cca0000000002c0d8a7000000000017a914ad1328a445664492aa448635cf48ddf742a04c9487a0160710000000001976a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac00000000',
     'fee': 0.001,
     'fee_per_kb': 0.0,
     'fee_per_kb_text': '0.00000000 MONA / 1 kB',
     'fee_text': '0.00100000 MONA',
     'locktime': datetime.datetime(2018, 3, 3, 11, 10, 56, 505764),
     'recipient_address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
     'refund_address': 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ',
     'secret': '6b4e4943623938384c72685a696b76336177424639436738616c58766737517058717466495639366f433353456c4d36634e71334c36636e42383632337a6a57',
     'secret_hash': '5de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b',
     'size': 256,
     'size_text': '256 bytes',
     'transaction_address': '11e4a28f469ed0d6171c6fb541327f9399b9e8ab416b19448de50538ad672601',
     'value': 0.11,
     'value_text': '0.11000000 MONA'}

     initial_transaction.publish()
     '11e4a28f469ed0d6171c6fb541327f9399b9e8ab416b19448de50538ad672601'
https://bchain.info/MONA/tx/11e4a28f469ed0d6171c6fb541327f9399b9e8ab416b19448de50538ad672601


## 4. Communication

[**Alice**] sends hers transaction hash `11e4a28f469ed0d6171c6fb541327f9399b9e8ab416b19448de50538ad672601` to Bob, so he could get `raw_transaction` (e.g. "hex" in raw data of https://bchain.info/MONA/tx/11e4a28f469ed0d6171c6fb541327f9399b9e8ab416b19448de50538ad672601).
And also she needs to send the contract to Bob (i.e. `63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704b0749a5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac`)


## 5. Contract audit

[**Bob**] needs to create contract in network of coins he wants to receive (i.e. Alice's network), in our case in Monacoin network.
And also at this point Bob should validate if the data returned in the contract is correct, he should also check if the transaction is present in the blockchain API (e.g. Bchain.info)

    alice_contract = mona_network.audit_contract(
        contract='63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704b0749a5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac',
        raw_transaction='0100000001fdbfc816109f4b8f94af5cb00e29f7a3a0ed7a80be671cebf630184c5b23cc9f000000008b483045022100b8ff6dffca1c42a8879c42dae6be9d65f3ba85e7abe9b8a1aefd526b7a39bbdb02207c5778bddc1d04c2018cc6a14c3be63855a9e130511d5180cab7b4124b1e99930141044fbe9cf6ef9bf4a13a693ee1d431eb700a592e8097619e0cfe82aff2a5c231e7154e464e4ec94201007b403b6de9a5819b0bc31eef0741c4fe6e932bca6d9cca0000000002c0d8a7000000000017a914ad1328a445664492aa448635cf48ddf742a04c9487a0160710000000001976a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac00000000',
    )
    alice_contract.show_details()

    {'contract_address': '3HU9muPrDbzm6f3B3pESkwd3gBx6Rafnd6',
     'locktime': datetime.datetime(2018, 3, 3, 11, 10, 56),
     'recipient_address': 'MAHnD7u7JD4DPA3R267zcB1xbaaiZrDRmL',
     'refund_address': 'MBriWYyfWNdrAmycN5otoUDWDMrdFK33DQ',
     'secret_hash': '5de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b',
     'transaction_address': '11e4a28f469ed0d6171c6fb541327f9399b9e8ab416b19448de50538ad672601',
     'value': 0.11,
     'value_text': '0.11000000 MONA'}


## 6. Participation

[**Bob**] has to create parallel transaction from point 3 but in his network (i.e. Dogecoin network). We call it `participate_transaction`.

    from clove.network.bitcoin.utxo import Utxo
    from clove.utils.bitcoin import from_base_units # blockcypher is showing value in satoshis

    dogecoins_to_swap = 100
    participate_utxo_list = [
        Utxo(
            tx_id='6bf80aed06436018357c1552dd89abcbe0a31907284ffd3c1a025584fc28c3d7',
            vout=1,
            value=from_base_units(98734979196),
            tx_script='76a91479364cbefe7c9b926792911b3611628102f9314c88ac',
        ),
    ]

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs the UTXOs can also be gathered automatically. For `chainz.cryptoid.info` API key is required - [read more](#cryptoid-api-key).

    participate_utxo_list = doge_network.get_utxo(bob_doge_wallet.address, dogecoins_to_swap)

With the list of UTXOs `particapate_transaction` can be created.

    participate_transaction = alice_contract.participate(
        'doge',
        bob_doge_wallet.address,
        alice_doge_address,
        dogecoins_to_swap,
        participate_utxo_list
    )

    participate_transaction.add_fee_and_sign(bob_doge_wallet)

    participate_transaction.show_details()

    {'contract': '63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a91462aef49943f16565b7ff9ef170a0d4bc5397763967041027995ab17576a91479364cbefe7c9b926792911b3611628102f9314c6888ac',
     'contract_address': 'A36T8zbAhfzozBCKpeGoGGKHbAmfn26bxD',
     'contract_transaction': '0100000001d7c328fc8455021a3cfd4f280719a3e0cbab89dd52157c3518604306ed0af86b010000008b483045022100b7f28aaa45662e9cb0d355b58e6d0f82d96a1a0245be5312015b7da9eb91f82502201f0d2566bd8c3f2f4da9ba341324a66b4b34957c191a228be0b4792310ebb945014104996266fc2984dee523d985d618da6f4609dd0054e0d6895e8d40278ddf3623f4d059edf51f5a8824623d96bd23d0fd5cc323e89aaa9af56f4afa408e34b7f04e000000000200e40b540200000017a91474e9cf2b2bdb70bb40b4bc3d48743f1e51548017877687f9a8140000001976a91479364cbefe7c9b926792911b3611628102f9314c88ac00000000',
     'fee': 0.00707846,
     'fee_per_kb': 0.02775866,
     'fee_per_kb_text': '0.02775866 DOGE / 1 kB',
     'fee_text': '0.00707846 DOGE',
     'locktime': datetime.datetime(2018, 3, 2, 11, 27, 28, 266577),
     'recipient_address': 'DE8tMBC9qk6a9A5T7NSdog4MJa16JqzZf7',
     'refund_address': 'DGC1MHWRaQeqn6MTeqkphzUHTeDnZgLvqs',
     'secret': '',
     'secret_hash': '5de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b',
     'size': 256,
     'size_text': '256 bytes',
     'transaction_address': 'c3a9474a1bb642e51fc10f14b2af2b5f57bef0858cd05116c9e53de783d92d36',
     'value': 100,
     'value_text': '100.00000000 DOGE'}

    participate_transaction.publish()
    'c3a9474a1bb642e51fc10f14b2af2b5f57bef0858cd05116c9e53de783d92d36'
https://live.blockcypher.com/doge/tx/c3a9474a1bb642e51fc10f14b2af2b5f57bef0858cd05116c9e53de783d92d36/

## 7. Communication

[**Bob**] sends his transaction hash `4168d4ac41debc550f6af6f5cb3ab37ab68aff624f562012a120379c026f6b12` and contract `63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a91462aef49943f16565b7ff9ef170a0d4bc5397763967041027995ab17576a91479364cbefe7c9b926792911b3611628102f9314c6888ac` to Alice.


## 8. Contract audit

[**Alice**] needs to audit contract in network of coins she wants to receive (i.e. Bob's network), in our case in Dogecoin network.
And also at this point Alice should validate if the data returned in the contract is correct, she should also check if the transaction is present in the blockchain API (e.g. Blockexplorer)

    bob_contract = doge_network.audit_contract(
        contract='63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a91462aef49943f16565b7ff9ef170a0d4bc5397763967041027995ab17576a91479364cbefe7c9b926792911b3611628102f9314c6888ac',
        raw_transaction='0100000001d7c328fc8455021a3cfd4f280719a3e0cbab89dd52157c3518604306ed0af86b010000008b483045022100b7f28aaa45662e9cb0d355b58e6d0f82d96a1a0245be5312015b7da9eb91f82502201f0d2566bd8c3f2f4da9ba341324a66b4b34957c191a228be0b4792310ebb945014104996266fc2984dee523d985d618da6f4609dd0054e0d6895e8d40278ddf3623f4d059edf51f5a8824623d96bd23d0fd5cc323e89aaa9af56f4afa408e34b7f04e000000000200e40b540200000017a91474e9cf2b2bdb70bb40b4bc3d48743f1e51548017877687f9a8140000001976a91479364cbefe7c9b926792911b3611628102f9314c88ac00000000'
    )
    bob_contract.show_details()

    {'contract_address': 'A36T8zbAhfzozBCKpeGoGGKHbAmfn26bxD',
     'locktime': datetime.datetime(2018, 3, 2, 11, 27, 28),
     'recipient_address': 'DE8tMBC9qk6a9A5T7NSdog4MJa16JqzZf7',
     'refund_address': 'DGC1MHWRaQeqn6MTeqkphzUHTeDnZgLvqs',
     'secret_hash': '5de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b',
     'transaction_address': 'c3a9474a1bb642e51fc10f14b2af2b5f57bef0858cd05116c9e53de783d92d36',
     'value': 100.0,
     'value_text': '100.00000000 DOGE'}


## 9. First redeem transaction

[**Alice**] can now collect coins she wants, thus she creates redeem transaction.

    alice_redeem = bob_contract.redeem(secret=initial_transaction.show_details()['secret'], wallet=alice_doge_wallet)
    alice_redeem.add_fee_and_sign()

    alice_redeem.show_details()

    {'fee': 0.01507825,
     'fee_per_kb': 0.03896189,
     'fee_per_kb_text': '0.03896189 DOGE / 1 kB',
     'fee_text': '0.01507825 DOGE',
     'recipient_address': 'DE8tMBC9qk6a9A5T7NSdog4MJa16JqzZf7',
     'size': 387,
     'size_text': '387 bytes',
     'transaction': '0100000001362dd983e73de5c91651d08c85f0be575f2bafb2140fc11fe542b61b4a47a9c300000000fd2c01483045022100e89b7a267c252419cf6dbeaa53d0074bce98e5a0d7da0c29ad4f31d8cd1ebfff0220495666315b45b4a5a30e2ea2cba1a20bae2031b607ff21230fea295cd35ce591014104dbe8366e39f93afcd70616e9049ee3eb5e09acdcadb63fb7d488fbb7af9f211e7e36998ba279f68ea01f5f090be8478465ee7dd91085e3f44831b0db032a63f7406b4e4943623938384c72685a696b76336177424639436738616c58766737517058717466495639366f433353456c4d36634e71334c36636e42383632337a6a57514c5d63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a91462aef49943f16565b7ff9ef170a0d4bc5397763967041027995ab17576a91479364cbefe7c9b926792911b3611628102f9314c6888ac00000000010fe2f453020000001976a91462aef49943f16565b7ff9ef170a0d4bc5397763988ac00000000',
     'transaction_address': '980ccfd7375a6946c3453178350784e5bf43a8216b039e513521805551a464dd',
     'value': 100.0,
     'value_text': '100.00000000 DOGE'}

    alice_redeem.publish()
    '980ccfd7375a6946c3453178350784e5bf43a8216b039e513521805551a464dd'
https://live.blockcypher.com/doge/tx/980ccfd7375a6946c3453178350784e5bf43a8216b039e513521805551a464dd/

[**Alice**] should get dogecoins just after redeem transaction is published.


## 10. Secret capture

[**Bob**] should check if his contract has been already redeemed to be able to extract the secret from the redeem transaction.

For networks supported by `blockcypher.com` or `chainz.cryptoid.info` APIs this can be done automatically.

    contract_address = bob_contract.show_details()['contract_address']
    secret = doge_network.extract_secret_from_redeem_transaction(contract_address)

For `chainz.cryptoid.info` API key is required - [read more](#cryptoid-api-key).

For unsupported networks Bob should extract the secret himself. First by using the `contract_address` he need to find [the contract](https://live.blockcypher.com/doge/address/A36T8zbAhfzozBCKpeGoGGKHbAmfn26bxD/) and the last transacion there (first from the top) will be the [redeem transaction](https://api.blockcypher.com/v1/doge/main/txs/980ccfd7375a6946c3453178350784e5bf43a8216b039e513521805551a464dd?limit=50&includeHex=true).

by using `hex` field (whole transaction)

    secret = doge_network.extract_secret(raw_transaction='0100000001362dd983e73de5c91651d08c85f0be575f2bafb2140fc11fe542b61b4a47a9c300000000fd2c01483045022100e89b7a267c252419cf6dbeaa53d0074bce98e5a0d7da0c29ad4f31d8cd1ebfff0220495666315b45b4a5a30e2ea2cba1a20bae2031b607ff21230fea295cd35ce591014104dbe8366e39f93afcd70616e9049ee3eb5e09acdcadb63fb7d488fbb7af9f211e7e36998ba279f68ea01f5f090be8478465ee7dd91085e3f44831b0db032a63f7406b4e4943623938384c72685a696b76336177424639436738616c58766737517058717466495639366f433353456c4d36634e71334c36636e42383632337a6a57514c5d63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a91462aef49943f16565b7ff9ef170a0d4bc5397763967041027995ab17576a91479364cbefe7c9b926792911b3611628102f9314c6888ac00000000010fe2f453020000001976a91462aef49943f16565b7ff9ef170a0d4bc5397763988ac00000000')

or `script` field from the first input:

    secret = doge_network.extract_secret(scriptsig='483045022100e89b7a267c252419cf6dbeaa53d0074bce98e5a0d7da0c29ad4f31d8cd1ebfff0220495666315b45b4a5a30e2ea2cba1a20bae2031b607ff21230fea295cd35ce591014104dbe8366e39f93afcd70616e9049ee3eb5e09acdcadb63fb7d488fbb7af9f211e7e36998ba279f68ea01f5f090be8478465ee7dd91085e3f44831b0db032a63f7406b4e4943623938384c72685a696b76336177424639436738616c58766737517058717466495639366f433353456c4d36634e71334c36636e42383632337a6a57514c5d63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a91462aef49943f16565b7ff9ef170a0d4bc5397763967041027995ab17576a91479364cbefe7c9b926792911b3611628102f9314c6888ac'

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
     'size': 387,
     'size_text': '387 bytes',
     'transaction': '0100000001012667ad3805e58d44196b41abe8b999937f3241b56f1c17d6d09e468fa2e41100000000fd2c01483045022100975ec541ce0395e7cf99fcf7d45203b9751df46b2fb26a561188d113ccd501cc02202e5005f90e1071227b8f07f4347e0d4fa8677edbe25710856611c16c3de7271e01410447408e366d0e979101f776ab10753091b0b62ba9aa609d006263959e030fb2d96e054c1f976a8cddcee5e1a95022cf289be89577ca348c893223d2e648de1abb406b4e4943623938384c72685a696b76336177424639436738616c58766737517058717466495639366f433353456c4d36634e71334c36636e42383632337a6a57514c5d63a8205de2198a39122100c4179933a4d577151445f400383aa6563d7fe2967cb54f8b8876a9141a376f6634e41c22b28bc9ef3336a623717083a46704b0749a5ab17576a9142b6a3314e8fcf1f1fd6b4d70b112bd5a192850576888ac00000000012052a600000000001976a9141a376f6634e41c22b28bc9ef3336a623717083a488ac00000000',
     'transaction_address': 'ea8f02ba968d2f764322453f4e3f9e78b8a257bb06dda28c6cc9e903949975a4',
     'value': 0.11,
     'value_text': '0.11000000 MONA'}

    bob_redeem.publish()
    'ea8f02ba968d2f764322453f4e3f9e78b8a257bb06dda28c6cc9e903949975a4'
https://bchain.info/MONA/tx/ea8f02ba968d2f764322453f4e3f9e78b8a257bb06dda28c6cc9e903949975a4


[**Bob**] should get monacoins just after redeem transaction is published.
