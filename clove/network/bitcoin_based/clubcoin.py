
from clove.network.bitcoin import Bitcoin


class ClubCoin(Bitcoin):
    """
    Class with all the necessary CLUB network information based on
    http://www.github.com/BitClubDev/ClubCoin/blob/master/src/chainparams.cpp
    (date of access: 02/11/2018)
    """
    name = 'clubcoin'
    symbols = ('CLUB', )
    seeds = ('seed1.clubcoin.io', 'seed2.clubcoin.io',
             'seed3.clubcoin.io', 'seed4.clubcoin.io', 'seed5.clubcoin.io')
    port = 18114
    message_start = b'\x70\x35\x42\x05'
    base58_prefixes = {
        'PUBKEY_ADDR': 28,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 153
    }
