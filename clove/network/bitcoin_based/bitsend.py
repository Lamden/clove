
from clove.network.bitcoin.base import BitcoinBaseNetwork


class BitSend(BitcoinBaseNetwork):
    """
    Class with all the necessary BSD network information based on
    http://www.github.com/LIMXTEC/BitSend/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'bitsend'
    symbols = ('BSD', )
    seeds = ()
    nodes = ('188.68.52.172', '37.120.186.85', '37.120.190.76',
             '213.136.80.93', '213.136.86.202', '213.136.86.205', '213.136.86.207')
    port = 8886
    message_start = b'\xa3\xd5\xc2\xf9'
    base58_prefixes = {
        'PUBKEY_ADDR': 102,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 204
    }
    source_code_url = 'http://www.github.com/LIMXTEC/BitSend/blob/master/src/chainparams.cpp'


class BitSendTestNet(BitSend):
    """
    Class with all the necessary BSD testing network information based on
    http://www.github.com/LIMXTEC/BitSend/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'test-bitsend'
    nodes = ()
    seeds = ('testnet-seed.bitsend.jonasschnelli.ch', 'seed.tbtc.petertodd.org',
             'testnet-seed.bluematt.me', 'testnet-seed.bitsend.schildbach.de')
    port = 18333
    message_start = b'\x0b\x11\x09\x07'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True
