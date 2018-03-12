from clove.network.bitcoin import Bitcoin


class CryptoBullion(Bitcoin):
    """
    Class with all the necessary CryptoBullion network information based on
    https://github.com/cryptogenicbonds/cryptobullion-cbx/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'cryptobullion'
    symbols = ('CBX', )
    seeds = ("seed.cryptobullion.io", )
    port = 7695
    message_start = b'\xe4\xe8\xe9\xe5'
    base58_prefixes = {
        'PUBKEY_ADDR': 11,
        'SCRIPT_ADDR': 8,
        'SECRET_KEY': 139
    }

# Has no Testnet
