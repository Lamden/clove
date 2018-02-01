from bitcoin.base58 import decode, encode
from bitcoin.core.key import CPubKey
from bitcoin.wallet import CBitcoinSecret
from pytest import mark, raises

from clove.network.bitcoin import BitcoinWallet


def test_password_encryption():
    wallet = BitcoinWallet()
    private_key = wallet.get_private_key()
    encrypted_private_key = BitcoinWallet.encrypt_private_key(
        private_key=private_key, password='test_password'
    )
    decrypted_private_key = BitcoinWallet.decrypt_private_key(
        encrypted_private_key=encrypted_private_key, password='test_password'
    )
    assert decrypted_private_key == private_key
    assert encrypted_private_key != private_key


@mark.parametrize('wallet', [
    BitcoinWallet(),
    BitcoinWallet(private_key='KxhniiXPCdBBpJmQnYPHmutKJq42Wm3yPY6AAKxvDPnTt8KA8BJF'),
    BitcoinWallet(
        encrypted_private_key=b'3bktZ1EG4dvKOilVbveJo8WoScrVJqGOfhjULdfooL'
                              b'CN7Il5Bu4CCA0HBP1k7iPZWyfohxiSdwJ3CpgHijIL2zb1THA=',
        password='test_password_xyz'
    )
])
def test_bitcoin_wallet(wallet):
    assert isinstance(wallet.private_key, CBitcoinSecret)
    assert isinstance(wallet.public_key, CPubKey)
    assert isinstance(wallet.get_address(), str)
    assert isinstance(wallet.get_private_key(), str)
    assert wallet.public_key == wallet.get_public_key()
    assert wallet.private_key.pub == wallet.public_key


def test_bitcoin_wallet_not_initialized_if_key_provided_whilst_password_not():
    with raises(
        TypeError,
        message="__init__() missing 'password' argument, since 'encrypted_private_key' argument was provided"
    ):
        BitcoinWallet(encrypted_private_key=b'C0RZlLtnrtozbxEHhTVZM')


def test_bitcoin_wallet_address_correct():
    address = BitcoinWallet().get_address()
    assert address.startswith('1')
    assert encode(decode(address)) == address
