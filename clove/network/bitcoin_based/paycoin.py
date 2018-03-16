from clove.network.bitcoin.base import BitcoinBaseNetwork


class PayCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary PayCoin network information based on
    https://github.com/PaycoinFoundation/paycoin/blob/master/src/net.cpp
    (date of access: 02/17/2018)
    """
    name = 'paycoin'
    symbols = ('XPY', )
    seeds = ("dnsseed.paycoin.com",
             "dnsseed.paycoinfoundation.org",
             "dnsseed.xpydev.org")

    port = 8998
    message_start = b'\xaa\xaa\xaa\xaa'
    base58_prefixes = {
        'PUBKEY_ADDR': 55,
        'SCRIPT_ADDR': 117,
        'SECRET_KEY': 183
    }
    source_code_url = 'https://github.com/PaycoinFoundation/paycoin/blob/master/src/net.cpp'
