import web3

from clove.network.ethereum import Ethereum


class EthereumClassic(Ethereum):
    """
    Class with all the necessary ETH network information and transaction building.
    """
    name = 'ethereum_classic'
    symbols = ('ETC',)
    seeds = (
        'https://mewapi.epool.io',
    )
    port = None

    # Contract is static on Ethereum rather than having to be built each time like on Bitcoin
    web3_connection = web3.Web3.HTTPProvider(seeds[0])
    contract_address = '0x0'
