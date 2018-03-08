from clove.network.bitcoin import Bitcoin


class Wexcoin(Bitcoin):
    """
    Class with all the necessary Wexcoin network information based on
    https://github.com/wexcoinofficial/wexcoin/blob/master/src/net.cpp
    (date of access: 02/18/2018)
    """
    name = 'wexcoin'
    symbols = ('WEX', )
    seeds = ()
    nodes = ("162.243.116.31",
             "192.241.251.204",
             "95.85.9.245",
             "95.85.14.64",
             "128.199.225.84",
             "128.199.158.215",
             "45.63.25.237",
             "45.32.33.53",
             "104.238.173.198",
             "104.238.191.11",
             "108.61.190.34",
             "45.63.43.96")
    port = 32714
    message_start = b'\xd3\xa1\x3e\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 76,
        'SCRIPT_ADDR': 35,
        'SECRET_KEY': 204
    }
