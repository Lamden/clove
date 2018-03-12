from clove.network.bitcoin import Bitcoin


class NPCcoin(Bitcoin):
    """
    Class with all the necessary NPCcoin network information based on
    https://github.com/npccoin/npccoin/blob/master/src/net.cpp
    (date of access: 02/17/2018)
    """
    name = 'npccoin'
    symbols = ('NPC', )
    seeds = ("seednode.npccoin.com", "seednode2.npccoin.com", )
    port = 26102
    message_start = b'\xb4\xb2\xd8\xe6'
    base58_prefixes = {
        'PUBKEY_ADDR': 53,
        'SCRIPT_ADDR': 85,
        'SECRET_KEY': 181
    }

# no testnet
