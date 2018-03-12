from clove.network.bitcoin import Bitcoin


class Influxcoin(Bitcoin):
    """
    Class with all the necessary Influxcoin network information based on
    https://github.com/chainworksindustries/influx/blob/master/src/net.cpp
    (date of access: 02/12/2018)
    """
    name = 'Influxcoin'
    symbols = ('INFX', )
    seeds = ("infx-seed01.chainworksindustries.com",
             "infx-seed02.chainworksindustries.com",
             "infx-seed03.chainworksindustries.com",
             "infx-seed04.chainworksindustries.com",
             "infx-seed05.chainworksindustries.com",
             "infx-seed06.chainworksindustries.com",
             "infx-seed07.chainworksindustries.com",
             "infx-seed08.chainworksindustries.com",
             "infx-seed09.chainworksindustries.com",
             "infx-seed10.chainworksindustries.com",
             "infx-seed11.chainworksindustries.com",
             "infx-seed12.chainworksindustries.com",
             "infx-seed13.chainworksindustries.com",
             "infx-seed14.chainworksindustries.com",
             "infx-seed15.chainworksindustries.com",
             "infx-seed16.chainworksindustries.com",
             "infx-seed17.chainworksindustries.com",
             "infx-seed18.chainworksindustries.com",
             "infx-seed19.chainworksindustries.com",
             "infx-seed20.chainworksindustries.com",
             "infx-seed21.chainworksindustries.com",
             "infx-seed22.chainworksindustries.com",
             "infx-seed23.chainworksindustries.com",
             "infx-seed24.chainworksindustries.com",
             "infx-seed25.chainworksindustries.com",
             "infx-seed26.chainworksindustries.com",
             "infx-seed27.chainworksindustries.com",
             "infx-seed28.chainworksindustries.com",
             "infx-seed29.chainworksindustries.com",
             "infx-seed30.chainworksindustries.com",
             "infx-seed31.chainworksindustries.com",
             "infx-seed32.chainworksindustries.com",
             "infx-seed33.chainworksindustries.com",
             "infx-seed34.chainworksindustries.com",
             "infx-seed35.chainworksindustries.com",
             "infx-seed36.chainworksindustries.com",
             "infx-seed37.chainworksindustries.com",
             "infx-seed38.chainworksindustries.com",
             "infx-seed39.chainworksindustries.com",
             "infx-seed40.chainworksindustries.com",
             "infx-seed41.chainworksindustries.com",
             "infx-seed42.chainworksindustries.com",
             "infx-seed43.chainworksindustries.com",
             "infx-seed44.chainworksindustries.com",
             "infx-seed45.chainworksindustries.com",
             "infx-seed46.chainworksindustries.com",
             "infx-seed47.chainworksindustries.com",
             "infx-seed48.chainworksindustries.com",
             "infx-seed49.chainworksindustries.com",
             "infx-seed50.chainworksindustries.com",
             "infx-seed51.chainworksindustries.com",
             "infx-seed52.chainworksindustries.com",
             "infx-seed53.chainworksindustries.com",
             "infx-seed54.chainworksindustries.com",
             "infx-seed55.chainworksindustries.com",
             "infx-seed56.chainworksindustries.com",
             "infx-seed57.chainworksindustries.com",
             "infx-seed58.chainworksindustries.com",
             "infx-seed59.chainworksindustries.com",
             "infx-seed60.chainworksindustries.com",
             "infx-seed61.chainworksindustries.com",
             "infx-seed62.chainworksindustries.com",
             "infx-seed63.chainworksindustries.com",
             "infx-seed64.chainworksindustries.com",
             "infx-seed65.chainworksindustries.com",
             "infx-seed66.chainworksindustries.com",
             "infx-seed67.chainworksindustries.com",
             "infx-seed68.chainworksindustries.com",
             "infx-seed69.chainworksindustries.com",
             "infx-seed70.chainworksindustries.com", )
    port = 9238
    message_start = b'\xf1\xe0\xa2\xd3'
    base58_prefixes = {
        'PUBKEY_ADDR': 102,
        'SCRIPT_ADDR': 28,
        'SECRET_KEY': 230
    }


# Has no Testnet
