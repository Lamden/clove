from clove.network.bitcoin.base import BitcoinBaseNetwork


class BitcoinGold(BitcoinBaseNetwork):
    """
    Class with all the necessary BTG network information based on
    https://github.com/BTCGPU/BTCGPU/blob/master/src/chainparams.cpp
    (date of access: 02/12/2018)
    """
    name = 'bitcoin-gold'
    symbols = ('BTG', )
    seeds = ('eu-dnsseed.bitcoingold-official.org',
             'dnsseed.bitcoingold.org', 'dnsseed.btcgpu.org')
    port = 8338
    message_start = b'\xe1\x47\x6d\x44'
    base58_prefixes = {
        'PUBKEY_ADDR': 38,
        'SCRIPT_ADDR': 23,
        'SECRET_KEY': 128
    }
    source_code_url = 'https://github.com/BTCGPU/BTCGPU/blob/master/src/chainparams.cpp'


class BitcoinGoldTestNet(BitcoinGold):
    """
    Class with all the necessary BTG testing network information based on
    https://github.com/BTCGPU/BTCGPU/blob/master/src/chainparams.cpp
    (date of access: 02/12/2018)
    """
    name = 'test-bitcoin-gold'
    seeds = ('eu-test-dnsseed.bitcoingold-official.org', 'test-dnsseed.bitcoingold.org',
             'test-dnsseed.btcgpu.org', 'btg.dnsseed.minertopia.org')
    port = 18338
    message_start = b'\xe1\x48\x6e\x45'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
