import hashlib

from clove.utils.hashing import generate_secret_with_hash


def test_generate_secret_with_hash():
    secret, secret_hash = generate_secret_with_hash()
    assert isinstance(secret, bytes)
    assert isinstance(secret_hash, bytes)
    assert len(secret) == 32
    assert len(secret_hash) == 20
    assert hashlib.new('ripemd160', secret).digest() == secret_hash
