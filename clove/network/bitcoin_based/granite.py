
from clove.network.bitcoin import Bitcoin


class Granite(Bitcoin):
    """
    Class with all the necessary GRN network information based on
    http://www.github.com/chrysophylax69/granite/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'granite'
    symbols = ('GRN', )
    seeds = (
        'grn-seed01.chainworksindustries.com', 'grn-seed02.chainworksindustries.com',
        'grn-seed03.chainworksindustries.com', 'grn-seed04.chainworksindustries.com',
        'grn-seed05.chainworksindustries.com', 'grn-seed06.chainworksindustries.com',
        'grn-seed07.chainworksindustries.com', 'grn-seed08.chainworksindustries.com',
        'grn-seed09.chainworksindustries.com', 'grn-seed10.chainworksindustries.com',
        'grn-seed11.chainworksindustries.com', 'grn-seed12.chainworksindustries.com',
        'grn-seed13.chainworksindustries.com', 'grn-seed14.chainworksindustries.com',
        'grn-seed15.chainworksindustries.com', 'grn-seed16.chainworksindustries.com',
        'grn-seed17.chainworksindustries.com', 'grn-seed18.chainworksindustries.com',
        'grn-seed19.chainworksindustries.com', 'grn-seed20.chainworksindustries.com',
        'grn-seed21.chainworksindustries.com', 'grn-seed22.chainworksindustries.com',
        'grn-seed23.chainworksindustries.com', 'grn-seed24.chainworksindustries.com',
    )
    port = 21777
    message_start = b'\xfe\xc3\xb9\xde'
    base58_prefixes = {
        'PUBKEY_ADDR': 38,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 166
    }
