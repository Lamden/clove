
from clove.network.bitcoin.base import BitcoinBaseNetwork


class AudioCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary ADC network information based on
    http://www.github.com/aurovine/audiocoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'audiocoin'
    symbols = ('ADC', )
    seeds = ()
    nodes = ('52.56.111.222', '52.56.175.189', '35.176.14.149', )
    port = 25159
    message_start = b'\xfa\xf4\xfb\xff'
    base58_prefixes = {
        'PUBKEY_ADDR': 23,
        'SCRIPT_ADDR': 125,
        'SECRET_KEY': 151
    }
    source_code_url = 'http://www.github.com/aurovine/audiocoin/blob/master/src/chainparams.cpp'


class AudioCoinTestNet(AudioCoin):
    """
    Class with all the necessary ADC testing network information based on
    http://www.github.com/aurovine/audiocoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-audiocoin'
    seeds = ('adcseed.presstab.pw', )
    nodes = ()
    port = 25159
    message_start = b'\xfa\xf4\xfb\xff'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
