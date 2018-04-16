from clove.network.bitcoin.base import BitcoinBaseNetwork


class MonetaryUnit(BitcoinBaseNetwork):
    """
    Class with all the necessary MonetaryUnit network information based on
    https://github.com/muecoin/MUECore/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'monetaryunit'
    symbols = ('MUE', )
    seeds = ("nodes.muex.io",
             "nodes.monetaryunit.org",
             "nodes.mymue.com",
             "nodes.cryptophi.com")
    port = 19683
    message_start = b'\xb5\xcc\xcd\xa7'
    base58_prefixes = {
        'PUBKEY_ADDR': 16,
        'SCRIPT_ADDR': 76,
        'SECRET_KEY': 126
    }
    source_code_url = 'https://github.com/muecoin/MUECore/blob/master/src/chainparams.cpp'


class MonetaryUnitTestNet(MonetaryUnit):
    """
    Class with all the necessary Diamond testing network information based on
    https://github.com/muecoin/MUECore/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'test-monetaryunit'
    seeds = ("tnodes.muex.io", )
    port = 18683
    message_start = b'\xbd\xa3\xc8\xb1'
    base58_prefixes = {
        'PUBKEY_ADDR': 38,
        'SCRIPT_ADDR': 19,
        'SECRET_KEY': 64
    }
    testnet = True
