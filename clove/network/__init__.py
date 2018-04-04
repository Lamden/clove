from clove.network.bitcoin import Bitcoin, BitcoinTestNet
from clove.network.bitcoin_based.aquariuscoin import AquariusCoin
from clove.network.bitcoin_based.audiocoin import AudioCoin, AudioCoinTestNet
from clove.network.bitcoin_based.bata import Bata, BataTestNet
from clove.network.bitcoin_based.bitcoin_cash import BitcoinCash, BitcoinCashTestNet
from clove.network.bitcoin_based.bitcoin_gold import BitcoinGold, BitcoinGoldTestNet
from clove.network.bitcoin_based.bitcore import Bitcore, BitcoreTestNet
from clove.network.bitcoin_based.bitmark import Bitmark
from clove.network.bitcoin_based.bitsend import BitSend, BitSendTestNet
from clove.network.bitcoin_based.blackcoin import BlackCoin
from clove.network.bitcoin_based.blocknet import Blocknet
from clove.network.bitcoin_based.creativecoin import CreativeCoin, CreativeCoinTestNet
from clove.network.bitcoin_based.dash import Dash, DashTestNet
from clove.network.bitcoin_based.digibyte import Digibyte
from clove.network.bitcoin_based.dopecoin import Dopecoin
from clove.network.bitcoin_based.egulden import EGulden, EGuldenTestNet
from clove.network.bitcoin_based.eternity import Eternity, EternityTestNet
from clove.network.bitcoin_based.europecoin import Europecoin
from clove.network.bitcoin_based.goldcoin import Goldcoin
from clove.network.bitcoin_based.greencoin import Greencoin
from clove.network.bitcoin_based.guncoin import Guncoin
from clove.network.bitcoin_based.i0coin import I0Coin
from clove.network.bitcoin_based.ivc_coin import IVCCoin
from clove.network.bitcoin_based.joulecoin import Joulecoin
from clove.network.bitcoin_based.komodo import Komodo
from clove.network.bitcoin_based.lanacoin import LanaCoin, LanaCoinTestNet
from clove.network.bitcoin_based.litecoin import Litecoin, LitecoinTestNet
from clove.network.bitcoin_based.machinecoin import Machinecoin, MachinecoinTestNet
from clove.network.bitcoin_based.monacoin import Monacoin, MonacoinTestNet
from clove.network.bitcoin_based.monetaryunit import MonetaryUnit, MonetaryUnitTestNet
from clove.network.bitcoin_based.mooncoin import Mooncoin
from clove.network.bitcoin_based.myriad import Myriad, MyriadTestNet
from clove.network.bitcoin_based.navcoin import Navcoin
from clove.network.bitcoin_based.netko import Netko
from clove.network.bitcoin_based.nevacoin import NevaCoin, NevaCoinTestNet
from clove.network.bitcoin_based.particl import Particl, ParticlTestNet
from clove.network.bitcoin_based.peercoin import Peercoin, PeercoinTestNet
from clove.network.bitcoin_based.pura import Pura
from clove.network.bitcoin_based.quark import Quark, QuarkTestNet
from clove.network.bitcoin_based.ravencoin import Ravencoin, RavencoinTestNet
from clove.network.bitcoin_based.rubycoin import Rubycoin
from clove.network.bitcoin_based.sexcoin import Sexcoin, SexcoinTestNet
from clove.network.bitcoin_based.skeincoin import Skeincoin
from clove.network.bitcoin_based.solarcoin import SolarCoin, SolarCoinTestNet
from clove.network.bitcoin_based.swagbucks import SwagBucks
from clove.network.bitcoin_based.syscoin import Syscoin
from clove.network.bitcoin_based.tajcoin import TajCoin
from clove.network.bitcoin_based.tao import Tao, TaoTestNet
from clove.network.bitcoin_based.vertcoin import Vertcoin, VertcoinTestNet
from clove.network.bitcoin_based.viacoin import Viacoin, ViacoinTestNet
from clove.network.bitcoin_based.visio import Visio
from clove.network.bitcoin_based.vivo import Vivo
from clove.network.bitcoin_based.zcoin import ZCoin, ZCoinTestNet
from clove.network.bitcoin_based.zetacoin import Zetacoin, ZetacoinTestNet
from clove.network.bitcoin_based.zoin import Zoin, ZoinTestNet
from clove.network.ethereum import Ethereum, EthereumTestnet

BITCOIN_BASED = (
    Bitcoin, BitcoinTestNet,
    AquariusCoin,
    AudioCoin, AudioCoinTestNet,
    Bata, BataTestNet,
    BitcoinCash, BitcoinCashTestNet,
    BitcoinGold, BitcoinGoldTestNet,
    Bitcore, BitcoreTestNet,
    Bitmark,
    BitSend, BitSendTestNet,
    BlackCoin,
    Blocknet,
    CreativeCoin, CreativeCoinTestNet,
    Dash, DashTestNet,
    Digibyte,
    Dopecoin,
    EGulden, EGuldenTestNet,
    Eternity, EternityTestNet,
    Europecoin,
    Goldcoin,
    Greencoin,
    Guncoin,
    I0Coin,
    IVCCoin,
    Joulecoin,
    Komodo,
    LanaCoin, LanaCoinTestNet,
    Litecoin, LitecoinTestNet,
    Machinecoin, MachinecoinTestNet,
    Monacoin, MonacoinTestNet,
    MonetaryUnit, MonetaryUnitTestNet,
    Mooncoin,
    Myriad, MyriadTestNet,
    Navcoin,
    Netko,
    NevaCoin, NevaCoinTestNet,
    Particl, ParticlTestNet,
    Peercoin, PeercoinTestNet,
    Pura,
    Quark, QuarkTestNet,
    Ravencoin, RavencoinTestNet,
    Rubycoin,
    Sexcoin, SexcoinTestNet,
    Skeincoin,
    SolarCoin, SolarCoinTestNet,
    SwagBucks,
    Syscoin,
    TajCoin,
    Tao, TaoTestNet,
    Vertcoin, VertcoinTestNet,
    Viacoin, ViacoinTestNet,
    Visio,
    Vivo,
    ZCoin, ZCoinTestNet,
    Zetacoin, ZetacoinTestNet,
    Zoin, ZoinTestNet,
)

ETHEREUM_BASED = (
    Ethereum, EthereumTestnet,
)


__all__ = BITCOIN_BASED + ETHEREUM_BASED
