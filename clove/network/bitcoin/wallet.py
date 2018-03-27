import base64
from hashlib import sha256

from Crypto import Random
from Crypto.Cipher import AES
from bitcoin.core.key import CPubKey
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress

from clove.utils.hashing import generate_secret_with_hash


class BitcoinWallet(object):

    def __init__(self, private_key=None, encrypted_private_key=None, password=None):
        if private_key is None and encrypted_private_key is None:
            _, secret_hash = generate_secret_with_hash()
            self.private_key = CBitcoinSecret.from_secret_bytes(secret=secret_hash)

        elif private_key is not None:
            self.private_key = CBitcoinSecret(private_key)

        elif encrypted_private_key is not None and password is not None:
            self.private_key = CBitcoinSecret(self.decrypt_private_key(encrypted_private_key, password))

        elif password is None:
            raise TypeError(
                "__init__() missing 'password' argument, since 'encrypted_private_key' argument was provided"
            )

        self.public_key = self.private_key.pub
        self.address = str(P2PKHBitcoinAddress.from_pubkey(self.public_key))

    def get_private_key(self) -> str:
        return str(self.private_key)

    def get_public_key(self) -> CPubKey:
        return self.public_key

    @staticmethod
    def encrypt_private_key(private_key: str, password: str) -> bytes:
        """Encrypt private key with the password."""
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(sha256(bytes(password.encode('utf-8'))).digest(), AES.MODE_CFB, iv)
        encrypted_private_key = base64.b64encode(iv + cipher.encrypt(bytes(private_key.encode('utf-8'))))
        return encrypted_private_key

    @staticmethod
    def decrypt_private_key(encrypted_private_key: bytes, password: str) -> str:
        """Decrypt private key with the password."""
        encrypted_private_key = base64.b64decode(encrypted_private_key)
        iv = encrypted_private_key[:AES.block_size]
        cipher = AES.new(sha256(bytes(password.encode('utf-8'))).digest(), AES.MODE_CFB, iv)
        private_key = cipher.decrypt(encrypted_private_key[AES.block_size:])
        return str(private_key, 'ascii')
