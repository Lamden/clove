import rlp
from web3 import Web3


class EthereumTransaction(object):

    def __init__(self, network, transaction):

        self.network = network
        self.tx = transaction

    @property
    def raw_transaction(self) -> str:
        return Web3.toHex(rlp.encode(self.tx))

    def show_details(self):
        details = self.tx.to_dict()
        value_text = Web3.fromWei(self.tx.value, 'ether')
        details['value_text'] = f'{value_text:.18f} {self.network.default_symbol}'
        return details

    def publish(self):
        try:
            self.network.web3.eth.sendRawTransaction(self.raw_transaction)
        except ValueError:
            return False
        return True


class EthereumAtomicSwapTransaction(EthereumTransaction):

    def __init__(self, network, transaction, secret: str=None, secret_hash: str=None):
        super().__init__(network, transaction)
        self.secret = secret
        self.secret_hash = secret_hash

    def show_details(self):
        details = super().show_details()
        details['secret'] = Web3.toHex(self.secret)
        details['secret_hash'] = Web3.toHex(self.secret_hash)
        return details
