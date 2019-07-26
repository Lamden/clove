from clove.utils.search import get_network_by_symbol

"""
Test Ethereum
"""
def test_Ethereum():
    # https://etherscan.io/address/0x49d77b4a97fbedfaa9526bdbe00ac0f0859ab91f
    network = get_network_by_symbol('ETH')
    ETH_wallet_address = '0x49d77B4a97fBEdFaA9526BDbE00Ac0f0859aB91f'

    assert network.get_balance( ETH_wallet_address ) == 2300000000000000


def test_Ethereum_testnet():
    # https://kovan.etherscan.io/address/0x796103e13616355790b2d325eb84ce1ed70db155
    network = get_network_by_symbol('ETH-TESTNET')
    ETH_testnet_wallet_address = '0x796103E13616355790b2d325eB84Ce1eD70Db155'

    assert network.get_balance( ETH_testnet_wallet_address ) == 5000000000000000


"""
Test Ethereum ERC20 Tokens
"""
def test_Ethereum_tokens():
    # https://kovan.etherscan.io/address/0x796103e13616355790b2d325eb84ce1ed70db155
    network = get_network_by_symbol('ETH')
    ETH_wallet_address = '0x49d77B4a97fBEdFaA9526BDbE00Ac0f0859aB91f'
    TAU_token_contract = '0xc27a2f05fa577a83ba0fdb4c38443c0718356501'

    assert network.get_balance( ETH_wallet_address, TAU_token_contract ) == 1000000000000000000

def test_Ethereum_Testnet_tokens():
    # https://kovan.etherscan.io/address/0x796103e13616355790b2d325eb84ce1ed70db155
    network = get_network_by_symbol('ETH-TESTNET')
    ETH_testnet_wallet_address = '0x25b8b1f2c21a70b294231c007e834ad2de04f51f'
    FUN_token_testnet_contract = '0x380bb65031fba2c9b8a3526302584a206e5bff41'

    assert network.get_balance( ETH_testnet_wallet_address, FUN_token_testnet_contract ) == 100000000000000


"""
Test Ethereum Based Networks
"""

"""
Explorer Down
def test_Ellaism():
    pass

    # 
    network = get_network_by_symbol('ELLA')

    assert network.get_balance( '????????????' ) == 0
"""

def test_Ethergem():
    # https://explorer.egem.io/addr/0xe233589351e607cf7ab33c7c2b72b3e3ebf062fb
    network = get_network_by_symbol('EGEM')

    assert network.get_balance( '0xe233589351e607cf7ab33c7c2b72b3e3ebf062fb' ) == 662883312914000000000

"""
WEB3 PROVIDER NOT WORKING
def test_EthereumClassic():
    # https://gastracker.io/addr/0x097738363b1662599ad0777e19461601f5ec8df9
    network = get_network_by_symbol('ETC')

    assert network.get_balance( '0x097738363B1662599ad0777E19461601F5EC8dF9' ) == 326105321792870
"""

def test_MusicCoin():
    # https://explorer.musicoin.org/account/0x8a69953c4c0c0547b57f77dd96f782be9464fe2d
    network = get_network_by_symbol('MUSIC')

    assert network.get_balance( '0x8a69953c4c0c0547b57f77dd96f782be9464fe2d' ) == 80126313574442000
"""
def test_Expanse():
    # https://gander.tech/address/0x3e641113891d12755f59003fbe96b91927370963
    network = get_network_by_symbol('EXP')

    assert network.get_balance( '0x3e641113891d12755f59003fbe96b91927370963' ) == 20000000000
"""
