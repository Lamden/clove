from clove.network import BITCOIN_BASED as BITCOIN_BASED
from clove.block_explorer.cryptoid import CryptoidAPI
from clove.utils.search import get_network_by_symbol

"""
Testing that CryptoID has an endpoint for all coins configured to use it
"""
def test_all_CryptoID():
    cryptoID_coins = CryptoidAPI.get_all_coins()
    no_CryptoID_endpoint = []
    
    for network in BITCOIN_BASED:
        if network.API == True:
            if 'https://chainz.cryptoid.info' == network.api_url:
                if network.symbols[0].lower() not in cryptoID_coins.keys():
                    no_CryptoID_endpoint.append(network.symbols[0])
                
    assert no_CryptoID_endpoint == []

"""
Test API is Live for CryptoID
"""
def test_CryptoID_API_isLive():
    # https://chainz.cryptoid.info/ltc/address.dws?LT7hW5QeBnbXz5ihPXToHJaGNRHWgnibZe.htm
    network = get_network_by_symbol('LTC')
    assert network.get_balance('LT7hW5QeBnbXz5ihPXToHJaGNRHWgnibZe') == 0.53420632


"""
Test InsiteAPI based coins
"""
def test_Bitcoin():
    # https://www.blockchain.com/btc/address/12c35gMcjsEidhufU9Pazg888HHjfJzjxQ
    network = get_network_by_symbol('BTC')
    assert network.get_balance('12c35gMcjsEidhufU9Pazg888HHjfJzjxQ') == 0.00009528

def test_BitcoinTestNet():
    # https://live.blockcypher.com/btc-testnet/address/n31RX4xTyvfJ1GubXCMWLRCrxa5UkZByrC/
    network = get_network_by_symbol('BTC-TESTNET')
    assert network.get_balance('n31RX4xTyvfJ1GubXCMWLRCrxa5UkZByrC') == 0.07450057

# Bitcon Based Tokens wit APIs
def test_BitcoinCash():
    # https://explorer.bitcoin.com/bch/address/bitcoincash:qq3q4leh6fn9099lcfwmrztr80msg2m9p5zln7hvqz
    network = get_network_by_symbol('BCH')
    assert network.get_balance('qq3q4leh6fn9099lcfwmrztr80msg2m9p5zln7hvqz') == 0.00059330

""" Needs upgrage to Insitev8 example: 
https://api.bitcore.io/api/BCH/mainnet/address/qq3q4leh6fn9099lcfwmrztr80msg2m9p5zln7hvqz/balance
def test_BitcoinCashTestNet():
    # https://blockexplorer.one/bitcoin-cash/testnet/address/qqyu6ngler7tqruhv5utc4kg6ct8j6qslukmz78ued
    network = get_network_by_symbol('BCH-TESTNET')
    assert network.get_balance('qqyu6ngler7tqruhv5utc4kg6ct8j6qslukmz78ued') == 0.00010000
"""

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



