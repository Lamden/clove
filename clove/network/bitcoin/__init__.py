from clove.network.bitcoin.base import BitcoinBaseNetwork


class Bitcoin(BitcoinBaseNetwork):
    """
    Class with all the necessary BTC network information based on
    https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'bitcoin'
    symbols = ('BTC', 'XBT')
    seeds = (
        'seed.bitcoin.sipa.be',
        'dnsseed.bluematt.me',
        'dnsseed.bitcoin.dashjr.org',
        'seed.bitcoinstats.com',
        'seed.bitcoin.jonasschnelli.ch',
        'seed.btc.petertodd.org',
    )
    port = 8333
    message_start = b'\xf9\xbe\xb4\xd9'
    base58_prefixes = {
        'PUBKEY_ADDR': 0,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }
    source_code_url = 'https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp'


class BitcoinTestNet(Bitcoin):
    """
    Class with all the necessary BTC testing network information based on
    https://github.com/bitcoin/bitcoin/blob/master/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-bitcoin'
    seeds = (
        'testnet-seed.bitcoin.jonasschnelli.ch',
        # 'seed.tbtc.petertodd.org', Last check: 2018-02-21
        'seed.testnet.bitcoin.sprovoost.nl',
        'testnet-seed.bluematt.me',
    )
    port = 18333
    message_start = b'\x0b\x11\x09\x07'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
