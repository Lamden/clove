from hashlib import sha256
from random import choices
from string import ascii_letters, digits


def generate_secret_with_hash() -> (bytes, bytes):
    secret = ''.join(choices(ascii_letters + digits, k=64))
    secret = bytes(secret.encode('utf-8'))

    secret_hash = sha256(secret).digest()

    return secret,  secret_hash
