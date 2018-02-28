# Clove atomic swap example


## Assumptions

* Alice has 3 bitcoins and wants to buy 10 litecoins
* Alice doesn't have a litecoin wallet
* Bob has 15 litecoins and wants to buy 2 bitcoins
* Bob has a bitcoin wallet


## 1. Wallets setup

[**Alice**] has to create a new litecoin wallet

    from clove.network import LitecoinTestNet

    ltc_network = LitecoinTestNet()

    alice_ltc_wallet = ltc_network.get_new_wallet()

    alice_ltc_wallet.address
    '1FiLXtspLcEU5uHr9mFDT556tXE8znTkxj'

    alice_ltc_wallet.get_private_key()
    'L15kFZg4MdoX2kqXEeEZMjbbVEdZzt1zL2vU59ynrtEf6GB16B3c'

[**Alice**] has to prepare her bitcoin wallet

    from clove.network import BitcoinTestNet

    btc_network = BitcoinTestNet()

    alice_btc_wallet = btc_network.get_wallet(private_key='cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe')

    alice_btc_wallet.address
    'msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM'

[**Bob**] can use his existing bitcoin wallet by passing his private key

    from clove.network import BitcoinTestNet

    btc_network = BitcoinTestNet()

    bob_btc_wallet = btc_network.get_wallet(private_key='cRoFBWMvcLXrLsYFt794NRBEPUgMLf5AmnJ7VQwiEenc34z7zSpK')

    bob_btc_wallet.address
    'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1'

[**Bob**] has to prepare his litecoin wallet

    from clove.network import LitecoinTestNet

    ltc_network = LitecoinTestNet()

    bob_ltc_wallet = ltc_network.get_wallet(private_key='cTVuBqcjryCdHiCfFxkY5ycNPH2RYNrbmgrTVXBsLKG8xR2My3j2')

    bob_ltc_wallet.address
    'muE6kHtUcKABwUWEkN47t5kWTMRM7NpnxV'

## 2. Communication

Alice and Bob exchange their wallet addresses.

## 3. Alice is initializing an atomic swap transaction

[**Alice**] has to prepare a transaction input (UTXO's that she wants to spend in this transaction). You can find these information by viewing transaction on block explorer e.g. [link](https://api.blockcypher.com/v1/btc/test3/txs/6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8?limit=50&includeHex=true)

    from clove.network.bitcoin import Utxo

    bitcoins_ammount = 2

    initial_utxo_list = [
        Utxo(
            tx_id='6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8',
            vout=1,
            value=2.78956946,
            tx_script='76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac'
        ),
    ]

    initial_transaction = btc_network.atomic_swap(
        alice_btc_wallet.address,
        bob_btc_wallet.address,
        bitcoins_ammount,
        initial_utxo_list
    )

    initial_transaction.add_fee_and_sign(alice_btc_wallet)

    initial_transaction.show_details()
    {'contract': '63a820260ab6c77d0f6e3108553b833712ab64e58368210dbe9914ce912dc9a82c8fc08876a9143f8870a5633e4fdac612fba47525fef082bbe961670a31353138313738363830b17576a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b6888ac',
     'contract_transaction': '0100000001b88ae2db0538ea2470b9b8f9cf80dbc5de9e90f1beeb70de6c971a8bd866cd6e010000006b483045022100803d409feeb1e1973fa95cfff7c52fa3dc1dd0017be2a13a0a5a6d28d012e26602203ce867a442a004a71571e6fa34a3151f1cb453ecc233c881592deec14cc3dcf6012103142762372a0f6f2b4718cdee32fa1a3cc2465d3379312e8875ee5f9193158177ffffffff0200c2eb0b000000006363a820260ab6c77d0f6e3108553b833712ab64e58368210dbe9914ce912dc9a82c8fc08876a9143f8870a5633e4fdac612fba47525fef082bbe961670a31353138313738363830b17576a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b6888ac7ab4b304000000001976a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac00000000',
     'contract_transaction_hash': 'bfad3cf3b16c8fb1b71ce88b1a48cb951d339abbb5720a94fbd4d6345ee6e64f',
     'fee': 0.00070936,
     'fee_per_kb': 0.00213021,
     'fee_per_kb_text': '0.00213021 BTC / 1 kB',
     'fee_text': '0.00070936 BTC',
     'locktime': datetime.datetime(2018, 2, 9, 13, 18, 0, 35873),
     'recipient_address': 'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1',
     'refund_address': 'msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM',
     'secret': '6e6f6d706752503031665755414b3678596b507637387535795a4a426a4669633748384c786f71494f5237687a37546e564c474e51566e634467354a72505569',
     'secret_hash': '260ab6c77d0f6e3108553b833712ab64e58368210dbe9914ce912dc9a82c8fc0',
     'size': 333,
     'size_text': '333 bytes',
     'value': 2,
     'value_text': '2.00000000 BTC'}

     initial_transaction.publish()
     'bfad3cf3b16c8fb1b71ce88b1a48cb951d339abbb5720a94fbd4d6345ee6e64f'


## 4. Communication

[**Alice**] sends hers transaction hash `bfad3cf3b16c8fb1b71ce88b1a48cb951d339abbb5720a94fbd4d6345ee6e64f` to Bob.


## 5. Contract audit

[**Bob**] needs to create contract in network of coins he wants to receive (i.e. Alice's network), in our case in Bitecoin network.
As Bob has transaction hash from Alice, he can get full serialized transaction. But for testing purposes we can get it from `initial_transaction` object.  
    
    alice_contract = btc_network.audit_contract(
        contract='63a820260ab6c77d0f6e3108553b833712ab64e58368210dbe9914ce912dc9a82c8fc08876a9143f8870a5633e4fdac612fba47525fef082bbe961670a31353138313738363830b17576a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b6888ac',
        raw_transaction='0100000001b88ae2db0538ea2470b9b8f9cf80dbc5de9e90f1beeb70de6c971a8bd866cd6e010000006b483045022100803d409feeb1e1973fa95cfff7c52fa3dc1dd0017be2a13a0a5a6d28d012e26602203ce867a442a004a71571e6fa34a3151f1cb453ecc233c881592deec14cc3dcf6012103142762372a0f6f2b4718cdee32fa1a3cc2465d3379312e8875ee5f9193158177ffffffff0200c2eb0b000000006363a820260ab6c77d0f6e3108553b833712ab64e58368210dbe9914ce912dc9a82c8fc08876a9143f8870a5633e4fdac612fba47525fef082bbe961670a31353138313738363830b17576a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b6888ac7ab4b304000000001976a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac00000000'
    )
    alice_contract.show_details()

    {'locktime': datetime.datetime(2018, 2, 24, 15, 36, 19),
     'recipient_address': 'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1',
     'refund_address': 'msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM',
     'secret_hash': '260ab6c77d0f6e3108553b833712ab64e58368210dbe9914ce912dc9a82c8fc0',
     'transaction_hash': 'bfad3cf3b16c8fb1b71ce88b1a48cb951d339abbb5720a94fbd4d6345ee6e64f',
     'value': 2,
     'value_text': '2.00000000 BTC'}
     
     
## 6. Participation 

[**Bob**] has to create parallel transaction from point 3 but in his network (i.e. Litecoin network). We call it `participate_transaction`.

    litecoin_ammount = 10
    participate_utxo_list = [
        Utxo(
            tx_id='326416caec1af6b18eda4cc9ef8c858b3d1905446f03223f8981d32523171bd8',
            vout=1,
            value=24.99964200,
            tx_script='76a9147ef1467725632defd311766e3dbb21e2014847cd88ac',
        ),
    ]
    participate_transaction = alice_contract.participate(
        'ltc',
        bob_ltc_wallet.address,
        alice_ltc_wallet.address,
        litecoin_ammount,
        participate_utxo_list
    )
    
    # For now add_fee_and_sign is not fully implemented for LTC network, hack this in such a way:
    participate_transaction.fee = 0.001
    participate_transaction.add_fee_and_sign(bob_ltc_wallet)
                                                             
    
    participate_transaction.show_details()
    {'contract': '63a8209fd0eef32d0a99db45200cac017140e24a9f29fd4b793a5a75bd1596d08a89b98876a9143dfd3bba567574ba0508d01a96e89300af292b066704d56f955ab17576a9147ef1467725632defd311766e3dbb21e2014847cd6888ac',
     'contract_transaction': '0100000001592390d5c9c19b7f2f27edfdd44043b4065e48ccdb67900145745d068221e5bd010000008a47304402205d83ec607e68d83187b3a45d42f2e27aadd1e41444973c8a8d72c8d58368bf94022046eb2af543207633dc57bd7c965985f578bbf8eaa6a601d0b482b432de50b23a01410443a2fbd871baafd35a6304fe9b93db0ec09f100631259feb933c2752b8fc8cf4ad8a04016345c17117146109dd69744fb32e8d032dd11a426f43a3fa76b403a60000000002005a6202000000005d63a8209fd0eef32d0a99db45200cac017140e24a9f29fd4b793a5a75bd1596d08a89b98876a9143dfd3bba567574ba0508d01a96e89300af292b066704d56f955ab17576a9147ef1467725632defd311766e3dbb21e2014847cd6888aca814a11a000000001976a9147ef1467725632defd311766e3dbb21e2014847cd88ac00000000',
     'fee': 0.001,
     'fee_per_kb': 0.0,
     'fee_per_kb_text': '0.00000000 LTC / 1 kB',
     'fee_text': '0.00100000 LTC',
     'locktime': datetime.datetime(2018, 2, 24, 15, 48, 53, 117091),
     'recipient_address': 'mmAisiQMtih4hEVe5xYtVJyQJSXHo7VWwM',
     'refund_address': 'ms6AUKhqnVgFppPjcLYkvRxEuy6cMqGL7P',
     'secret': '',
     'secret_hash': '9fd0eef32d0a99db45200cac017140e24a9f29fd4b793a5a75bd1596d08a89b9',
     'size': 358,
     'size_text': '358 bytes',
     'transaction_hash': '4168d4ac41debc550f6af6f5cb3ab37ab68aff624f562012a120379c026f6b12',
     'value': 10,
     'value_text': '10.00000000 LTC'}
    
    participate_transaction.publish()
   
 
## 7. Communication

[**Bob**] sends his transaction hash `4168d4ac41debc550f6af6f5cb3ab37ab68aff624f562012a120379c026f6b12` to Alice.


## 8. Contract audit

[**Alice**] needs to create contract in network of coins she wants to receive (i.e. Bob's network), in our case in Litecoin network.
As Alice has transaction hash from Bob, she can get full serialized transaction. But for testing purposes we can get it from `participate_transaction` object.  
    
    bob_contract = ltc_network.audit_contract(
        contract='63a8209fd0eef32d0a99db45200cac017140e24a9f29fd4b793a5a75bd1596d08a89b98876a9143dfd3bba567574ba0508d01a96e89300af292b066704d56f955ab17576a9147ef1467725632defd311766e3dbb21e2014847cd6888ac'
        raw_transaction='0100000001592390d5c9c19b7f2f27edfdd44043b4065e48ccdb67900145745d068221e5bd010000008a47304402205d83ec607e68d83187b3a45d42f2e27aadd1e41444973c8a8d72c8d58368bf94022046eb2af543207633dc57bd7c965985f578bbf8eaa6a601d0b482b432de50b23a01410443a2fbd871baafd35a6304fe9b93db0ec09f100631259feb933c2752b8fc8cf4ad8a04016345c17117146109dd69744fb32e8d032dd11a426f43a3fa76b403a60000000002005a6202000000005d63a8209fd0eef32d0a99db45200cac017140e24a9f29fd4b793a5a75bd1596d08a89b98876a9143dfd3bba567574ba0508d01a96e89300af292b066704d56f955ab17576a9147ef1467725632defd311766e3dbb21e2014847cd6888aca814a11a000000001976a9147ef1467725632defd311766e3dbb21e2014847cd88ac00000000'
    )
    bob_contract.show_details()
    
    {'locktime': datetime.datetime(2018, 2, 24, 15, 48, 53),
     'recipient_address': 'mmAisiQMtih4hEVe5xYtVJyQJSXHo7VWwM',
     'refund_address': 'ms6AUKhqnVgFppPjcLYkvRxEuy6cMqGL7P',
     'secret_hash': '9fd0eef32d0a99db45200cac017140e24a9f29fd4b793a5a75bd1596d08a89b9',
     'transaction_hash': '4168d4ac41debc550f6af6f5cb3ab37ab68aff624f562012a120379c026f6b12',
     'value': 10.0,
     'value_text': '10.00000000 LTC'}


## 9. First redeem transaction

[**Alice**] can now collect coins she wants, thus she creates redeem transaction.
    
    alice_redeem = bob_contract.redeem(secret=initial_transaction.show_details()['secret'], wallet=alice_ltc_wallet)
    alice_redeem.add_fee_and_sign()
    
    alice_redeem.show_details()
    
    {'locktime': datetime.datetime(2018, 2, 24, 15, 55, 42),
     'transaction': '0100000001222d497dd12edf372cd814bb0f09b958a511e002838343af8891f86ab758542e00000000fd2c014830450221009d1b15bf348b3965bae8da424765c1e1ce11911011e0f0e8a865e1401782c96602202e68592fe6308c10c7a225009a0e5548e5f4115555081fa9a96939d305ab54fb01410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4406950564e32496a76383243546a523966704f3945464e5239736932446373453367596649776f365357626b4e4176516d436b5164387878633534554453645948514c5d63a82088e65ab63c0aceb81187eabfd45594268ce6d565d42ed0963fbef48e88d89a158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045ba4965ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac0000000001b80c0400000000001976a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac00000000',
     [some other key-values]...}
     
    alice_redeem.publish()
    
[**Alice**] should get litecoins just after redeem transaction is published.
    
    
## 10. Secret capture

[**Bob**] Bob should track Alice's wallet and search for redeem transaction (Alice can but don't have to send him a transaction address).
Then Bob should extract the secret himself from that transaction.

    secret = ltc_network.extract_secret('0100000001222d497dd12edf372cd814bb0f09b958a511e002838343af8891f86ab758542e00000000fd2c014830450221009d1b15bf348b3965bae8da424765c1e1ce11911011e0f0e8a865e1401782c96602202e68592fe6308c10c7a225009a0e5548e5f4115555081fa9a96939d305ab54fb01410459cdb91eb7298bc2578dc4e7ac2109ac3cfd9dc9818795c5583e720d2114d540724bf26b4541f683ff51968db627a04eecd1f5cff615b6350dad5fb595f8adf4406950564e32496a76383243546a523966704f3945464e5239736932446373453367596649776f365357626b4e4176516d436b5164387878633534554453645948514c5d63a82088e65ab63c0aceb81187eabfd45594268ce6d565d42ed0963fbef48e88d89a158876a91485c0522f6e23beb11cc3d066cd20ed732648a4e667045ba4965ab17576a914621f617c765c3caa5ce1bb67f6a3e51382b8da296888ac0000000001b80c0400000000001976a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac00000000')
    
## 11. Second redeem transaction

[**Bob**] can now collect coins he wants, thus he creates redeem transaction.

    bob_redeem = alice_contract.redeem(secret=secret, wallet=bob_btc_wallet)
    bob_redeem.add_fee_and_sign()
    bob_redeem.publish()

[**Bob**] should get bitcoins just after redeem transaction is published.
