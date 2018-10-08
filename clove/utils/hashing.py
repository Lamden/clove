import hashlib
import secrets


def generate_secret_with_hash() -> (bytes, bytes):
    '''
    Generating secret and related ripemd160 hash.

    Returns:
        tuple: secret, secret hash

    Example:
        >>> from clove.utils.hashing import generate_secret_with_hash
        >>> secret, secret_hash = generate_secret_with_hash()
        >>> secret.hex()
        '95a968aa18866ffe6ed9ad39a06e27a90e55699734007173bfdd3daa4bab661d'
    '''
    secret = secrets.token_bytes(32)
    secret_hash = hashlib.new('ripemd160', secret).digest()
    return secret, secret_hash
