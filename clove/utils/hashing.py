import hashlib
import secrets


def generate_secret_with_hash() -> (bytes, bytes):
    secret = secrets.token_bytes(32)
    secret_hash = hashlib.new('ripemd160', secret).digest()
    return secret, secret_hash
