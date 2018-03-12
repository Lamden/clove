from clove.network.bitcoin import Bitcoin


class Sterlingcoin(Bitcoin):
    """
    Class with all the necessary Sterlingcoin (SLG) network information based on
    https://github.com/Sterlingcoin/Sterlingcoin-1.6.0.1-Release/blob/master/src/net.cpp
    (date of access: 02/17/2018)
    """
    name = 'sterlingcoin'
    symbols = ('SLG', )
    seeds = (
        'seed1.sterlingcoin.org.uk',
        'seed2.sterlingcoin.org.uk',
        'cwi-seed01.sterlingcoin.org',
        'cwi-seed02.sterlingcoin.org',
        'cwi-seed03.sterlingcoin.org',
        'cwi-seed04.sterlingcoin.org',
        'cwi-seed05.sterlingcoin.org',
        'cwi-seed06.sterlingcoin.org',
        'cwi-seed07.sterlingcoin.org',
        'cwi-seed08.sterlingcoin.org',
        'cwi-seed09.sterlingcoin.org',
        'cwi-seed10.sterlingcoin.org',
        'cwi-seed11.sterlingcoin.org',
        'cwi-seed12.sterlingcoin.org',
        'cwi-seed13.sterlingcoin.org',
        'cwi-seed14.sterlingcoin.org',
        'cwi-seed15.sterlingcoin.org',
        'cwi-seed16.sterlingcoin.org',
        'cwi-seed17.sterlingcoin.org',
        'cwi-seed18.sterlingcoin.org',
        'cwi-seed19.sterlingcoin.org',
        'cwi-seed20.sterlingcoin.org',
        'cwi-seed21.sterlingcoin.org',
        'cwi-seed22.sterlingcoin.org',
        'cwi-seed23.sterlingcoin.org',
        'cwi-seed24.sterlingcoin.org',
        'cwi-seed25.sterlingcoin.org'
    )
    port = 1141
    message_start = b'\x70\x35\x22\x05'
    base58_prefixes = {
        'PUBKEY_ADDR': 63,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 191
    }

# no testnet
