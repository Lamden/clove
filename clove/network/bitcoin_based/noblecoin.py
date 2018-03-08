from clove.network.bitcoin import Bitcoin


class NobleCoin(Bitcoin):
    """
    Class with all the necessary NobleCoin network information based on
    https://github.com/noblecoinnobl/noblecoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'noblecoin'
    symbols = ('NOBL', )
    seeds = ('nobl.poolerino.com', )
    port = 55884
    message_start = b'\xc0\xdb\xf1\xfd'
    base58_prefixes = {
        'PUBKEY_ADDR': 21,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 149
    }


# Has no testnet
