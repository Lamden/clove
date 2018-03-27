from datetime import datetime, timedelta
from typing import Optional

from ethereum.transactions import Transaction
import rlp
from web3 import Web3

from clove.utils.hashing import generate_secret_with_hash


class EthereumTransaction(object):

    def __init__(self, network):

        self.network = network
        self.tx = None

    @property
    def raw_transaction(self) -> str:
        return Web3.toHex(rlp.encode(self.tx))

    def show_details(self):
        details = self.tx.to_dict()
        value_text = Web3.fromWei(self.tx.value, 'ether')
        details['value_text'] = f'{value_text:.18f} {self.network.default_symbol}'
        return details

    def sign(self, private_key):
        return self.tx.sign(private_key)

    def publish(self) -> Optional[str]:
        try:
            self.network.web3.eth.sendRawTransaction(self.raw_transaction)
        except ValueError:
            return
        return Web3.toHex(self.tx.hash)


class EthereumAtomicSwapTransaction(EthereumTransaction):
    init_hours = 48
    participate_hours = 24

    def __init__(
        self,
        network: str,
        sender_address: str,
        recipient_address: str,
        value: int,
        secret_hash: str=None,
        token_address: str=None,
        gas_price: int=None,
        gas_limit: int=None,
    ):
        super().__init__(network)

        self.sender_address = network.unify_address(sender_address)
        self.recipient_address = network.unify_address(recipient_address)
        self.secret = None
        self.secret_hash = secret_hash
        self.value = value
        self.gas_price = gas_price
        self.gas_limit = gas_limit
        self.set_locktime()
        self.set_secrets()

        if token_address:
            self.token_address = self.network.unify_address(sender_address)
            self.contract_address = self.network.token_swap_contract_address
            self.abi = self.network.token_abi
        else:
            self.contract_address = self.network.eth_swap_contract_address
            self.abi = self.network.eth_abi

        self.set_contract()

    def set_secrets(self):

        if self.secret_hash:
            try:
                self.secret_hash.hex()
            except SyntaxError:
                raise ValueError('Incorrect value of secret_hash argument')
        else:
            self.secret, self.secret_hash = generate_secret_with_hash()

    def set_locktime(self):
        self.locktime = datetime.utcnow() + timedelta(hours=24 if self.secret_hash else 48)
        self.locktime_unix = int(self.locktime.timestamp())

    def set_contract(self):
        self.contract = self.network.web3.eth.contract(address=self.contract_address, abi=self.abi)

        initiate_func = self.contract.functions.initiate(
            self.locktime_unix,
            self.secret_hash,
            self.recipient_address,
        )

        tx_dict = {
            'nonce': self.network.web3.eth.getTransactionCount(self.sender_address),
            'from': self.sender_address,
            'value': self.value,
        }

        if self.gas_price:
            tx_dict['gasPrice'] = self.gas_price

        tx_dict = initiate_func.buildTransaction(tx_dict)

        if not self.gas_limit:
            self.gas_limit = initiate_func.estimateGas({
                key: value for key, value in tx_dict.items() if key not in ('to', 'data')
            })

        self.tx = Transaction(
            nonce=tx_dict['nonce'],
            gasprice=tx_dict['gasPrice'],
            startgas=self.gas_limit,
            to=tx_dict['to'],
            value=tx_dict['value'],
            data=Web3.toBytes(hexstr=tx_dict['data']),
        )

    def show_details(self):
        details = super().show_details()
        details['secret'] = self.secret.hex()
        details['secret_hash'] = self.secret_hash.hex()
        details['locktime'] = self.locktime
        details['gas_limit'] = self.gas_limit
        details['sender_address'] = self.sender_address
        details['recipient_address'] = self.recipient_address
        details['transaction_address'] = details.pop('hash')
        details['contract_address'] = self.contract_address
        details['refund_address'] = self.sender_address
        return details
