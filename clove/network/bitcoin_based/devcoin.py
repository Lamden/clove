from clove.network.bitcoin import Bitcoin


class Devcoin(Bitcoin):
    """
    Class with all the necessary Devcoin network information based on
    https://github.com/coinzen/devcoin/blob/master/src/net.cpp
    (date of access: 02/14/2018)
    """
    name = 'devcoin'
    symbols = ('DVC', )
    seeds = ("dvc.public.txn.co.in",
             "dvc-seed.21stcenturymoneytalk.org",
             "dvcstable01.devtome.com",
             "dvcstable01.dvcnode.org",
             "dvcstable02.dvcnode.org",
             "dvcstable03.dvcnode.org",
             "dvcstable04.dvcnode.org",
             "dvcstable05.dvcnode.org",
             "dvcstable06.dvcnode.org",
             "dvcstable07.dvcnode.org",
             "node01.dvcnode.com",
             "node02.dvcnode.com",
             "node03.dvcnode.com")
    port = 52333
    message_start = b'dev-'
    base58_prefixes = {
        'PUBKEY_ADDR': 0,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 128
    }

# Has no testnet
