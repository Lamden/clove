from clove.network.bitcoin.base import BitcoinBaseNetwork


class SmileyCoin(BitcoinBaseNetwork):
    """
    Class with all the necessary SmileyCoin network information based on
    https://github.com/tutor-web/smileyCoin/blob/post-2017-wallet/src/chainparams.cpp
    (date of access: 02/18/2018)
    """
    name = 'smileycoin'
    symbols = ('SMLY', )
    seeds = ("dnsseed.smileyco.in", )
    port = 11337
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 25,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 153
    }
    source_code_url = 'https://github.com/tutor-web/smileyCoin/blob/post-2017-wallet/src/chainparams.cpp'

# no testnet
