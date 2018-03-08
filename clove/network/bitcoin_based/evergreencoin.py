from clove.network.bitcoin import Bitcoin


class EverGreenCoin(Bitcoin):
    """
    Class with all the necessary EverGreenCoin network information based on
    https://github.com/evergreencoindev/evergreencoin/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'evergreencoin'
    symbols = ('EGC', )
    seeds = ("seed.evergreencoin.org",
             "seed2.evergreencoin.org",
             "cwi-seed01.evergreencoin.org",
             "cwi-seed02.evergreencoin.org",
             "cwi-seed03.evergreencoin.org",
             "cwi-seed04.evergreencoin.org",
             "cwi-seed05.evergreencoin.org",
             "cwi-seed06.evergreencoin.org",
             "cwi-seed07.evergreencoin.org",
             "cwi-seed08.evergreencoin.org",
             "cwi-seed09.evergreencoin.org",
             "cwi-seed10.evergreencoin.org",
             "cwi-seed11.evergreencoin.org",
             "cwi-seed12.evergreencoin.org",
             "cwi-seed13.evergreencoin.org",
             "cwi-seed14.evergreencoin.org",
             "cwi-seed15.evergreencoin.org",
             "cwi-seed16.evergreencoin.org",
             "cwi-seed17.evergreencoin.org",
             "cwi-seed18.evergreencoin.org",
             "cwi-seed19.evergreencoin.org",
             "cwi-seed20.evergreencoin.org",
             "cwi-seed21.evergreencoin.org",
             "cwi-seed22.evergreencoin.org",
             "cwi-seed23.evergreencoin.org",
             "cwi-seed24.evergreencoin.org",
             "cwi-seed25.evergreencoin.org")
    port = 5757
    message_start = b'\x21\x24\x62\x47'
    base58_prefixes = {
        'PUBKEY_ADDR': 33,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 161
    }


# Has no Testnet
