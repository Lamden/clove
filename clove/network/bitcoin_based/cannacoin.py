from clove.network.bitcoin import Bitcoin


class CannaCoin(Bitcoin):
    """
    Class with all the necessary CannaCoin network information based on
    https://github.com/Cannacoin-Project/Cannacoin/blob/Proof-of-Stake/src/net.cpp
    (date of access: 02/14/2018)
    """
    name = 'cannacoin'
    symbols = ('CCN', )
    seeds = ("dnsseed.cannacoin.cc",
             "seed1.cannacoin.cc",
             "seed2.cannacoin.cc",
             "seed3.cannacoin.cc",
             "seed4.cannacoin.cc",
             "seed5.cannacoin.cc")
    port = 7143
    message_start = b'\xc7\xc0\xfc\xd5'
    base58_prefixes = {
        'PUBKEY_ADDR': 28,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 156
    }


class CannaCoinTestNet(CannaCoin):
    """
    Class with all the necessary CannaCoin testing network information based on
    https://github.com/Cannacoin-Project/Cannacoin/blob/Proof-of-Stake/src/net.cpp
    (date of access: 02/14/2018)
    """
    name = 'test-cannacoin'
    seeds = ("testnet.cannacoin.cc", )
    port = 17143
    message_start = b'\xfc\xc1\xb7\xdc'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
