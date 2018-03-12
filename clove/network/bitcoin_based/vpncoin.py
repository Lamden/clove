from clove.network.bitcoin import Bitcoin


class VPNCoin(Bitcoin):
    """
    Class with all the necessary VPNCoin (VASH) network information based on
    https://github.com/Bit-Net/vash/blob/master/src/net.cpp
    (date of access: 02/17/2018)
    """
    name = 'vpncoin'
    symbols = ('VASH', )
    seeds = (
        'seed.vpncoin.org', 'node.vpncoin.org', 'pool.vpncoin.org', 's4.vpncoin.org', 's5.vpncoin.org',
        's6.vpncoin.org', 's7.vpncoin.org', 's8.vpncoin.org', 's9.vpncoin.org', 'abe.vpncoin.org', 'faucet.vpncoin.org',
        's1.bitnet.cc', 's2.bitnet.cc', 's3.bitnet.cc', 's4.bitnet.cc', 's5.bitnet.cc', 's6.bitnet.cc', 's7.bitnet.cc',
        's8.bitnet.cc', 's9.bitnet.cc'
    )
    port = 1920
    message_start = b'\x70\x35\x22\x05'
    base58_prefixes = {
        'PUBKEY_ADDR': 71,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 199
    }

# no testnet
