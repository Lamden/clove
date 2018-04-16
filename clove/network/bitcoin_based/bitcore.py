
from clove.network.bitcoin.base import BitcoinBaseNetwork


class Bitcore(BitcoinBaseNetwork):
    """
    Class with all the necessary BTX network information based on
    http://www.github.com/LIMXTEC/BitCore/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'bitcore'
    symbols = ('BTX', )
    seeds = ()
    nodes = ('188.68.52.172', '37.120.186.85', '37.120.190.76', )
    port = 8555
    message_start = b'\xf9\xbe\xb4\xd9'
    base58_prefixes = {
        'PUBKEY_ADDR': 0,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }
    source_code_url = 'http://www.github.com/LIMXTEC/BitCore/blob/master/src/chainparams.cpp'


class BitcoreTestNet(Bitcore):
    """
    Class with all the necessary BTX testing network information based on
    http://www.github.com/LIMXTEC/BitCore/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-bitcore'
    seeds = ('dnsseed1.bitcore.org', 'dnsseed2.bitcore.org')
    nodes = ()
    port = 18333
    message_start = b'\x0b\x11\x09\x07'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
