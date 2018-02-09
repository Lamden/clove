# Clove atomic swap example


## Assumptions

* Alice has 3 bitcoins and wants to buy 10 litecoins
* Alice doesn't have a litecoin wallet
* Bob has 15 litecoins and wants to buy 2 bitcoins
* Bob has a bitcoin wallet


## 1. Wallets setup

[**Alice**] have to create a new litecoin wallet

    from clove.network import LitecoinTestNet

    ltc_network = LitecoinTestNet()

    alice_ltc_wallet = ltc_network.get_new_wallet()

    alice_ltc_wallet.get_address()
    '1FiLXtspLcEU5uHr9mFDT556tXE8znTkxj'

    alice_ltc_wallet.get_private_key()
    'L15kFZg4MdoX2kqXEeEZMjbbVEdZzt1zL2vU59ynrtEf6GB16B3c'

[**Alice**] have to prepare her bitcoin wallet

    from clove.network import BitcoinTestNet

    btc_network = BitcoinTestNet()

    alice_btc_wallet = btc_network.get_wallet(private_key='cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe')

    alice_btc_wallet.get_address()
    'msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM'

[**Bob**] can use his existing bitcoin wallet by passing his private key

    from clove.network import BitcoinTestNet

    btc_network = BitcoinTestNet()

    bob_btc_wallet = btc_network.get_wallet(private_key='cRoFBWMvcLXrLsYFt794NRBEPUgMLf5AmnJ7VQwiEenc34z7zSpK')

    bob_btc_wallet.get_address()
    'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1'

[**Bob**] have to prepare his litecoin wallet

    from clove.network import LitecoinTestNet

    ltc_network = LitecoinTestNet()

    bob_ltc_wallet = ltc_network.get_wallet(private_key='cTVuBqcjryCdHiCfFxkY5ycNPH2RYNrbmgrTVXBsLKG8xR2My3j2')

    bob_ltc_wallet.get_address()
    'muE6kHtUcKABwUWEkN47t5kWTMRM7NpnxV'

## 2. Communication

Alice and Bob exchange their wallet addresses.

## 3. Alice is initializing an atomic swap transaction

[**Alice**] have to prepare a transaction input (UTXO's that she wants to spend in this transaction). You can find these information by viewing transaction on block explorer e.g. [link](https://api.blockcypher.com/v1/btc/test3/txs/6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8?limit=50&includeHex=true)

    from clove.network.bitcoin import Utxo

    bob_btc_address = 'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1'

    bitcoins_ammount = 2

    solvable_utxo = [
        Utxo(
            tx_id='6ecd66d88b1a976cde70ebbef1909edec5db80cff9b8b97024ea3805dbe28ab8',
            vout=1,
            value=2.78956946,
            tx_script='76a914812ff3e5afea281eb3dd7fce9b077e4ec6fba08b88ac'
        ),
    ]

    transaction = btc_network.initiate_atomic_swap(
        alice_btc_wallet.get_address(),
        bob_btc_address,
        bitcoins_ammount,
        solvable_utxo
    )

    transaction.add_fee_and_sign(alice_btc_wallet)

    transaction.show_details()
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

     transaction.publish()
     'bfad3cf3b16c8fb1b71ce88b1a48cb951d339abbb5720a94fbd4d6345ee6e64f'


## 4. Communication

[**Alice**] sends her transaction hash `bfad3cf3b16c8fb1b71ce88b1a48cb951d339abbb5720a94fbd4d6345ee6e64f` to Bob.
