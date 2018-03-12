from clove.network.bitcoin import Bitcoin


class DollarOnline(Bitcoin):
    """
    Class with all the necessary DollarOnline network information based on
    https://github.com/dollar-online/dollar/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'dollaronline'
    symbols = ('DOLLAR', )
    seeds = ()
    nodes = ("91.109.38.231", )
    port = 22888
    message_start = b'\xa1\xa0\xa2\xa3'
    base58_prefixes = {
        'PUBKEY_ADDR': 30,
        'SCRIPT_ADDR': 90,
        'SECRET_KEY': 158
    }


# No Testnet
