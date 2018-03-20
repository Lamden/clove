from clove.network.bitcoin.base import BitcoinBaseNetwork


class AquariusCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary ARCO network information based on
    http://www.github.com/AquariusNetwork/ARCO/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'aquariuscoin'
    symbols = ('ARCO', )
    seeds = (
        'node1.aquariuscoin.com', 'node2.aquariuscoin.com', 'node3.aquariuscoin.com',
        'node4.aquariuscoin.com', 'node5.aquariuscoin.com', 'node6.aquariuscoin.com',
        'node7.aquariuscoin.com', 'node8.aquariuscoin.com', 'node9.aquariuscoin.com',
        'node.bit-coin.pw'
    )
    port = 6205
    message_start = b'\x93\x30\x64\xc7'
    base58_prefixes = {
        'PUBKEY_ADDR': 23,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 151
    }
    source_code_url = 'http://www.github.com/AquariusNetwork/ARCO/blob/master/src/chainparams.cpp'
