# Tips & Tricks

## Gathering UTXO

For Bitcoin-based networks there are two ways to create UTXO list: automated and manual.

### Automated

This method is used behind the scene in the `atomic_swap()` method when the `solvable_utxo` argument hasn't been passed.

    from clove.network import Litecoin

    network = Litecoin()

    utxo = network.get_utxo(address='LUAn5PWmsPavgz32mGkqsUuAKncftS37Jq', amount='0.01')

    utxo
    [
        Utxo(
            tx_id='0cd90567497823097d03464b4b2d08dd659f1c5621dd55e9540bc9bcd3e191ec',
            vout='0',
            value='0.00976168',
            tx_script='76a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac',
            wallet=None,
            secret=None,
            refund=False
        ),
        Utxo(
            tx_id='a5c027027c695f403fe570850e35ffd44bb28479ecaaee039372015fe0aae7b2',
            vout='0',
            value='0.00097114',
            tx_script='76a91485c0522f6e23beb11cc3d066cd20ed732648a4e688ac',
            wallet=None,
            secret=None,
            refund=False
        )
    ]


### Manual

If some network doesn't have block explorer integration to gather UTXO automatically you can still create it manually by getting required data (`tx_id`, `vout`, `value` and `tx_script`) from some other source.

    from clove.network.bitcoin.utxo import Utxo

    utxo_list = [
        Utxo(
            tx_id='5d920e7093b2f0ac94cb1c13a42a79ed1c1290fcc4155d15a123d69b1afe05d2',
            vout=1,
            value=2.086,
            tx_script='76a9142b6a3314e8fcf1f1fd6b4d70b112bd5a1928505788ac'
        ),
    ]

and then you can use this list in atomic swap transaction.

    network.atomic_swap(
        sender_address=alice_address,
        recipient_address=bob_address,
        value=1.5,
        solvable_utxo=utxo_list,
    )


## Getting fee

In Bitcoin-base networks every transaction needs to include some small fee for miners. Fee depends on several factors and is changing over time.

### via Clove API

The easiest way to get current fee is to ask Clove API via `get_current_fee_per_kb` method. Clove API is a proxy between you and block explorer with a cache layer so you will not be exposed to requests limits in some block explorers.

    from clove.network import Bitcoin

    network = Bitcoin()
    network.get_current_fee_per_kb()
    0.00014827


### via block explorer

You can omit the Clove API and calculate fee directly from network's block explorer

    from clove.network import Mooncoin

    network = Mooncoin()
    network.get_fee()
    0.00200369

some of those networks supports also counting fee from a given number of last transactions

    network.get_fee(tx_limit=20)
    0.00200362


### Setting fee manually

If you want to suggest your own fee value you can do this directly by setting `transaction.fee`.

    transaction.fee = 0.005
    transaction.add_fee()
    transaction.sign(SOME_WALLET)


## Publishing custom transactions

Even if you have non atomic swap transaction you can still use clove for publishing.

    raw_transaction = '010000000184a38a4e8743964249665fb241fbd3...35b'
    network.publish(raw_transaction)


## Getting transaction details

Using clove you can check details of every transaction.

    from clove.network import Mooncoin

    network = Mooncoin()
    network.get_transaction('675e379fa2e0ce4853b8d33ee13d90eb1cdc71aecdf94ecf455d3b7cf04577ac')
    {'block': 1358589,
     'confirmations': 72,
     'fees': 0.000654,
     'hash': '675e379fa2e0ce4853b8d33ee13d90eb1cdc71aecdf94ecf455d3b7cf04577ac',
     'index': 2,
     'inputs': [{'addr': '2ZqW69xn69cLSqRjdaCgyCutmVtpGc5hy5',
       'amount': 5655.451082,
       'received_from': {'n': 0,
        'tx': 'f7d5e6eb642db342647017621bda3c3f78ccb1338cf10d2a0ae90bd606582c26'}}],
     'outputs': [{'addr': '2PtewZ6yPQUyb3ATgUnUH5kaLHhNm9QupF',
       'amount': 5650.170428,
       'script': '76a914774ef2ad06c0bf967b55b5e221af795d01e66bd388ac'},
      {'addr': '2Z1cWuzCzWAxo1BumMiiqDd7k5jpv5JvGk',
       'amount': 0.76,
       'script': '76a914db58f7b45d5555bff1b49a7a79e6e1cb25eb558288ac'},
      {'addr': '2VQFxhq4LFRu2wfq2gP6btve2MiVwuiXsm',
       'amount': 2.04,
       'script': '76a914b3c0df73140cc787723252cc9f7c0db04953023188ac'},
      {'addr': '2MzTQt2GuGd7fx1aT4vsBWQDg2uh1aLKGQ',
       'amount': 0.6,
       'script': '76a9146277917f54f218d4723452a307f7134542db079688ac'},
      {'addr': '2bimR99ZxpyeTxVeRrtoE4V3eEbUaDdLgD',
       'amount': 1.88,
       'script': '76a914f911b40d716f6a2da724cb333cccdb4f2546fb7688ac'}],
     'timestamp': 1539000366,
     'total_input': 5655.451082,
     'total_output': 5655.450428}


## Getting balance

To check balance of a given wallet or contract just use

    from clove.network import BitcoinTestNet

    network = BitcoinTestNet()
    network.get_balance('msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM')
    4.22188744
