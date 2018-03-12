from clove.network.bitcoin import Bitcoin


class MasterSwiscoin(Bitcoin):
    """
    Class with all the necessary Master Swiscoin network information based on
    https://github.com/SCNPay/Swiscoin-Master/blob/master/src/net.cpp
    (date of access: 02/17/2018)
    """
    name = 'master_swiscoin'
    symbols = ('MSCN', )
    seeds = ("swisexplorer.com",
             "dns.swisexplorer.com")
    port = 20774
    message_start = b'\xb6\xfe\xe0\xc5'
    base58_prefixes = {
        'PUBKEY_ADDR': 125,
        'SCRIPT_ADDR': 20,
        'SECRET_KEY': 253
    }

# no testnet
