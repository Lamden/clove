from clove.network.bitcoin import Bitcoin


class Piggycoin(Bitcoin):
    """
    Class with all the necessary Piggycoin network information based on
    https://github.com/piggycoin/newpiggycoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'piggycoin'
    symbols = ('PIGGY', )
    seeds = ("piggynodes.piggy-coin.com",
             "piggynodes.piggyfacts.com",
             "piggynodes.blockpunk.com",
             "piggynodes.neurocis.me")
    port = 54481
    message_start = b'\xa1\xa0\xa2\xa3'
    base58_prefixes = {
        'PUBKEY_ADDR': 118,
        'SCRIPT_ADDR': 28,
        'SECRET_KEY': 246
    }


# Has no testnet
