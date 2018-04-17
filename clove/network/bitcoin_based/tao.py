from clove.network.bitcoin.base import BitcoinBaseNetwork


class Tao(BitcoinBaseNetwork):
    """
    Class with all the necessary Tao (XTO) network information based on
    https://github.com/taoblockchain/tao-core/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'tao'
    symbols = ('XTO', )
    seeds = ('taoexplorer.com', 'seed1.tao.network', 'seed2.tao.network', 'seed3.tao.network',
             'seed4.tao.network', 'seed5.tao.network', 'seed6.tao.network')
    port = 15150
    message_start = b'\x1d\xd1\x1e\xe1'
    base58_prefixes = {
        'PUBKEY_ADDR': 66,
        'SCRIPT_ADDR': 3,
        'SECRET_KEY': 76
    }
    source_code_url = 'https://github.com/taoblockchain/tao-core/blob/master/src/chainparams.cpp'


class TaoTestNet(Tao):
    """
    Class with all the necessary Tao (XTO) testing network information based on
    https://github.com/taoblockchain/tao-core/blob/master/src/chainparams.cpp
    (date of access: 02/17/2018)
    """
    name = 'test-tao'
    seeds = ('testnet.tao.network', )
    port = 16160
    message_start = b'\x2f\xca\x4d\x3e'
    base58_prefixes = {
        'PUBKEY_ADDR': 127,
        'SCRIPT_ADDR': 130,
        'SECRET_KEY': 138
    }
    testnet = True
