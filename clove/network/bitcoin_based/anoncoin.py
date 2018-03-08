from clove.network.bitcoin import Bitcoin


class Anoncoin(Bitcoin):
    """
    Class with all the necessary Anoncoin network information based on
    https://github.com/Anoncoin/anoncoin/blob/master/src/chainparams.cpp
    (date of access: 02/13/2018)
    """
    name = 'Anoncoin'
    symbols = ('ANC', )
    seeds = ("seed.frank2.net",
             "dnsseed03.anoncoin.net",
             "anc.dnsseed01.anoncoin.darkgamex.ch")
    port = 9377
    message_start = b'\xfa\xca\xba\xda'
    base58_prefixes = {
        'PUBKEY_ADDR': 23,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 151
    }


# No testnet
