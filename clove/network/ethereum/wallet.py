from ecdsa import SECP256k1, SigningKey
from ethereum import utils


class EthereumWallet(object):
    '''Ethereum wallet object.'''

    def __init__(self, private_key=None):
        self.private_key = private_key
        if private_key is None:
            self.private_key = SigningKey.generate(curve=SECP256k1).to_string().hex()
        self._raw_address = utils.privtoaddr(self.private_key)
        self.address = utils.checksum_encode(self._raw_address)
