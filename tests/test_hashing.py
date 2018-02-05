from hashlib import sha256

from clove.utils.hashing import generate_secret_with_hash


def test_generate_secret_with_hash():
    secret, secret_hash = generate_secret_with_hash()
    assert isinstance(secret, bytes)
    assert isinstance(secret_hash, bytes)
    assert sha256(secret).digest() == secret_hash
