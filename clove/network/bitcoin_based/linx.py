from clove.network.bitcoin import Bitcoin


class Linx(Bitcoin):
    """
    Class with all the necessary Linx network information based on
    https://github.com/linX-project/linX/blob/master/src/net.cpp
    (date of access: 02/16/2018)
    """
    name = 'linx'
    symbols = ('LINX', )
    seeds = ("seed.mylinx.io",
             "seed1.mylinx.io",
             "seed2.mylinx.io",
             "seed3.mylinx.io",
             "seed4.mylinx.io",
             "seed5.mylinx.io")
    port = 13925
    message_start = b'\x23\xb2\xa3\xcb'
    base58_prefixes = {
        'PUBKEY_ADDR': 75,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 203
    }


class LinxTestNet(Linx):
    """
    Class with all the necessary Linx testing network information based on
    https://github.com/linX-project/linX/blob/master/src/net.cpp
    (date of access: 02/16/2018)
    """
    name = 'test-linx'
    seeds = ("testnet.mylinx.io",
             "testnet1.mylinx.io",
             "testnet2.mylinx.io",
             "testnet3.mylinx.io",
             "testnet4.mylinx.io",
             "testnet5.mylinx.io",
             "testlinx.ffptech.com")
    port = 24915
    message_start = b'\xdc\xd4\xb7\xdc'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
