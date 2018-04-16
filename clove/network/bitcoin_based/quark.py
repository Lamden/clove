from clove.network.bitcoin.base import BitcoinBaseNetwork


class Quark(BitcoinBaseNetwork):
    """
    Class with all the necessary Quark (QRK) network information based on
    https://github.com/quark-project/quark/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'quark'
    symbols = ('QRK', )
    seeds = ('seed1.qrknet.info', 'seed2.qrknet.info', 'seed3.qrknet.info', 'seed4.qrknet.info',
             'seed5.qrknet.info', 'seed6.qrknet.info', 'seed7.qrknet.info', 'seed8.qrknet.info')
    port = 11973
    message_start = b'\xfe\xa5\x03\xdd'
    base58_prefixes = {
        'PUBKEY_ADDR': 58,
        'SCRIPT_ADDR': 9,
        'SECRET_KEY': 186
    }
    source_code_url = 'https://github.com/quark-project/quark/blob/master/src/chainparams.cpp'


class QuarkTestNet(Quark):
    """
    Class with all the necessary Quark (QRK) testing network information based on
    https://github.com/quark-project/quark/blob/master/src/chainparams.cpp
    (date of access: 02/16/2018)
    """
    name = 'test-quark'
    seeds = ('testseed1.qrknet.info', )
    port = 21973
    message_start = b'\x01\x1a\x39\xf7'
    base58_prefixes = {
        'PUBKEY_ADDR': 119,
        'SCRIPT_ADDR': 199,
        'SECRET_KEY': 247
    }
    testnet = True
