from clove.network.bitcoin import Bitcoin


class DotCoin(Bitcoin):
    """
    Class with all the necessary DotCoin network information based on
    https://github.com/cryptopianz/dot/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'dotcoin'
    symbols = ('DOT', )
    seeds = ("nodes1.cryptopia.co.nz", "nodes2.cryptopia.co.nz",
             "pools1.cryptopia.co.nz", "pools2.cryptopia.co.nz")
    port = 19745
    message_start = b'\x16\x6f\x4f\x5d'
    base58_prefixes = {
        'PUBKEY_ADDR': 0,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }


# Has no Testnet
