from clove.network.bitcoin import Bitcoin, BitcoinTestNet
from clove.network.bitcoin_based.bitcoin_cash import BitcoinCash, BitcoinCashTestNet
from clove.network.bitcoin_based.bitcoin_gold import BitcoinGold, BitcoinGoldTestNet
from clove.network.bitcoin_based.litecoin import Litecoin, LitecoinTestNet

from clove.network.ethereum import Ethereum, EthereumTestnet
from clove.network.ethereum_based.ellaism import Ellaism, EllaismTestnet
from clove.network.ethereum_based.ether_gem import EtherGem
from clove.network.ethereum_based.ethereum_classic import EthereumClassic
from clove.network.ethereum_based.expanse import Expanse
from clove.network.ethereum_based.musicoin import Musicoin

BITCOIN_BASED = (
    Bitcoin, BitcoinTestNet,
    BitcoinCash, BitcoinCashTestNet,
    BitcoinGold, BitcoinGoldTestNet,
    Litecoin, LitecoinTestNet,
)

ETHEREUM_BASED = (
    Ellaism, EllaismTestnet,
    Ethereum, EthereumTestnet,
    EthereumClassic,
    EtherGem,
    Expanse,
    Musicoin,
)


__all__ = BITCOIN_BASED + ETHEREUM_BASED
