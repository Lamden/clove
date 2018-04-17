from clove.network.bitcoin.base import BitcoinBaseNetwork


class EGulden(BitcoinBaseNetwork):
    """
    Class with all the necessary eGulden (EFL) network information based on
    https://github.com/Electronic-Gulden-Foundation/egulden/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'egulden'
    symbols = ('EFL', )
    seeds = (
        'dnsseed1.egulden.org',
        'dnsseed2.egulden.org',
        'dnsseed3.egulden.org',
        'dnsseed4.egulden.org',
        'dnsseed5.egulden.org',
        'dnsseed6.egulden.org',
        'dnsseed7.egulden.org',
        'dnsseed8.egulden.org',
        'dnsseed9.egulden.org',
        'dnsseed10.egulden.org'
    )
    port = 11015
    message_start = b'\x80\x83\x4c\x30'
    base58_prefixes = {
        'PUBKEY_ADDR': 48,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 176
    }
    source_code_url = 'https://github.com/Electronic-Gulden-Foundation/egulden/blob/master/src/chainparams.cpp'


class EGuldenTestNet(EGulden):
    """
    Class with all the necessary eGulden (EFL) testing network information based on
    https://github.com/Electronic-Gulden-Foundation/egulden/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'test-egulden'
    seeds = ('testnetseed1.egulden.org', )
    port = 5744
    message_start = b'\x80\x83\x4c\x31'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
