from clove_api.components import Network
from clove.utils.search import get_network_by_symbol
from clove.network.base import BaseNetwork

# Bitcon
def test_Bitcoin():
    network = get_network_by_symbol('BTC')
    assert network.get_balance('12c35gMcjsEidhufU9Pazg888HHjfJzjxQ') == 0.00009528

def test_BitcoinTestNet():
    network = get_network_by_symbol('BTC-TESTNET')
    assert network.get_balance('n31RX4xTyvfJ1GubXCMWLRCrxa5UkZByrC') == 0.07450057

# Bitcon Based Tokens wit APIs
def test_BitcoinCash():
    # https://explorer.bitcoin.com/bch/address/bitcoincash:qq3q4leh6fn9099lcfwmrztr80msg2m9p5zln7hvqz
    network = get_network_by_symbol('BCH')
    assert network.get_balance('qq3q4leh6fn9099lcfwmrztr80msg2m9p5zln7hvqz') == 0.00059330

def test_BitcoinGold():
    # https://explorer.bitcoingold.org/insight/address/GVK4S5HHMBcEbATd1Hgiv5wgRKvbFyJaSe
    network = get_network_by_symbol('BTG')
    assert network.get_balance('GVK4S5HHMBcEbATd1Hgiv5wgRKvbFyJaSe') == 0.00056972

def test_Dash():
    # https://chainz.cryptoid.info/dash/address.dws?XccPicDbg7HhRfFwPU3Z2CFVpHSYAhuxtu.htm
    network = get_network_by_symbol('DASH')
    assert network.get_balance('XccPicDbg7HhRfFwPU3Z2CFVpHSYAhuxtu') == 0.00208369

def test_Ravencoin():
    # https://explorer.ravencoin.world/address/RHwb533S2BRL3ac8L872hXKLHsrE94fcrk
    network = get_network_by_symbol('RVN')
    assert network.get_balance('RHwb533S2BRL3ac8L872hXKLHsrE94fcrk') == 1.00090000

def test_RavencoinTestNet():
    # https://testnet.ravencoin.network/address/mzeGFKD9Zs7oH2WwAkqCm1uewJg2j2urDs
    network = get_network_by_symbol('RVN-TESTNET')
    assert network.get_balance('mzeGFKD9Zs7oH2WwAkqCm1uewJg2j2urDs') == 2.10566468

def test_Litecoin():
    # https://chainz.cryptoid.info/ltc/address.dws?LT7hW5QeBnbXz5ihPXToHJaGNRHWgnibZe.htm
    network = get_network_by_symbol('LTC')
    assert network.get_balance('LT7hW5QeBnbXz5ihPXToHJaGNRHWgnibZe') == 0.53420632 

# Endpoints down
"""
def test_Monacoin():  
    # https://bchain.info/MONA/addr/MR7j9VSw88Unie49yuwe9nVxq2mvkANSRG
    network = get_network_by_symbol('MONA')
    assert network.get_balance('bcda9b15700258280cccc4e4299c55cf6838e3fc') == 43.71 

def test_BitcoinCashTestNet():
    # https://explorer.bitcoin.com/tbch/address/n1rawFCdBRjMCQSRKv9w2x2wup5NzkW2bq
    network = get_network_by_symbol('BCH-TESTNET')
    assert network.get_balance('n1rawFCdBRjMCQSRKv9w2x2wup5NzkW2bq') == 0.10000000

"""


# No Endpoint
"""
def test_LitecoinTestNet():
    # https://chainz.cryptoid.info/ltc/address.dws?LT7hW5QeBnbXz5ihPXToHJaGNRHWgnibZe.htm
    network = get_network_by_symbol('LTC-TESTNET')
    assert network.get_balance('n3knqHtFLP8KBtrWvdcqCE1s6yfsq5GKBe') == 10.52304139
"""



"""
def test_AquariusCoin():
def test_AudioCoin():
def test_Bata():
def test_BataTestNet():
def test_BitcoinGoldTestNet():     
def test_Bitcore():      
def test_BitcoreTestNet():     
def test_Bitmark():     
def test_BitSend():      
def test_BitSendTestNet():     
def test_BlackCoin():     
def test_Blocknet():     
def test_CreativeCoin():      
def test_CreativeCoinTestNet():         
def test_DashTestNet():     
def test_Digibyte():     
def test_Dopecoin():     
def test_EGulden():      
def test_EGuldenTestNet():     
def test_Eternity():      
def test_EternityTestNet():     
def test_Europecoin():     
def test_Goldcoin():     
def test_Greencoin():     
def test_Guncoin():     
def test_I0Coin():     
def test_IVCCoin():     
def test_Joulecoin():     
def test_Komodo():     
def test_LanaCoin():      
def test_LanaCoinTestNet():     
def test_Litecoin():      
def test_LitecoinTestNet():     
def test_Machinecoin():      
def test_MachinecoinTestNet():         
def test_MonacoinTestNet():     
def test_MonetaryUnit():      
def test_MonetaryUnitTestNet():     
def test_Mooncoin():     
def test_Myriad():      
def test_MyriadTestNet():     
def test_Navcoin():     
def test_Netko():     
def test_NevaCoin():      
def test_NevaCoinTestNet():     
def test_Particl():      
def test_ParticlTestNet():     
def test_Peercoin():      
def test_PeercoinTestNet():     
def test_Pura():     
def test_Quark():      
def test_QuarkTestNet():      
def test_Rubycoin():     
def test_Sexcoin():      
def test_SexcoinTestNet():     
def test_Skeincoin():     
def test_SolarCoin():      
def test_SolarCoinTestNet():     
def test_SwagBucks():     
def test_Syscoin():     
def test_TajCoin():     
def test_Tao():      
def test_TaoTestNet():     
def test_Vertcoin():      
def test_VertcoinTestNet():     
def test_Viacoin():      
def test_ViacoinTestNet():     
def test_Visio():     
def test_Vivo():     
def test_ZCoin():      
def test_ZCoinTestNet():     
def test_Zetacoin():      
def test_ZetacoinTestNet():     
def test_Zoin():      
def test_ZoinTestNet():     
"""