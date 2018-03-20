from clove.network.bitcoin.base import BitcoinBaseNetwork


class Theresamaycoin(BitcoinBaseNetwork):
    """
    Class with all the necessary Theresa May Coin (MAY) network information based on
    https://github.com/zulufourm1ke/theresamaycoin-v1.0.1.0/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'theresamaycoin'
    symbols = ('MAY', )
    seeds = ()
    nodes = ('86.53.121.36', )
    port = 35010
    message_start = b'\xa4\xd2\xf8\xa6'
    base58_prefixes = {
        'PUBKEY_ADDR': 50,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 178
    }
    source_code_url = 'https://github.com/zulufourm1ke/theresamaycoin-v1.0.1.0/blob/master/src/net.cpp'
