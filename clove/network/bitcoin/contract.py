from datetime import datetime
from typing import Optional

from bitcoin.core import b2lx, b2x, script
from bitcoin.wallet import CBitcoinAddress, P2PKHBitcoinAddress

from clove.network.bitcoin.transaction import BitcoinTransaction
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import auto_switch_params, from_base_units


class BitcoinContract(object):
    '''Atomic Swap contract.'''

    @auto_switch_params(1)
    def __init__(
        self,
        network,
        contract: str,
        raw_transaction: Optional[str]=None,
        transaction_address: Optional[str]=None
    ):

        if not raw_transaction and not transaction_address:
            raise ValueError('Provide raw_transaction or transaction_address argument.')

        self.network = network
        self.symbol = self.network.default_symbol
        self.contract = contract
        self.tx = None
        self.vout = None
        self.confirmations = None
        self.tx_address = transaction_address
        if raw_transaction:
            self.tx = self.network.deserialize_raw_transaction(raw_transaction)
            try:
                self.vout = self.tx.vout[0]
            except IndexError:
                raise ValueError('Given transaction has no outputs.')
        else:
            tx_json = self.network.get_transaction(transaction_address)
            if not tx_json:
                raise ValueError('No transaction found under given address.')

            self.vout = self.network.get_first_vout_from_tx_json(tx_json)
            self.confirmations = self.network.get_confirmations_from_tx_json(tx_json)

        if not self.vout:
            raise ValueError('Given transaction has no outputs.')

        contract_tx_out = self.vout
        contract_script = script.CScript.fromhex(self.contract)
        script_pub_key = contract_script.to_p2sh_scriptPubKey()
        valid_p2sh = script_pub_key == contract_tx_out.scriptPubKey
        self.address = str(CBitcoinAddress.from_scriptPubKey(script_pub_key))
        try:
            self.balance = self.network.get_balance(self.address)
        except NotImplementedError:
            self.balance = None

        script_ops = list(contract_script)
        if valid_p2sh and self.is_valid_contract_script(script_ops):
            self.recipient_address = str(P2PKHBitcoinAddress.from_bytes(script_ops[6]))
            self.refund_address = str(P2PKHBitcoinAddress.from_bytes(script_ops[13]))
            self.locktime_timestamp = int.from_bytes(script_ops[8], byteorder='little')
            self.locktime = datetime.utcfromtimestamp(self.locktime_timestamp)
            self.secret_hash = b2x(script_ops[2])
            self.value = from_base_units(contract_tx_out.nValue)
        else:
            raise ValueError('Given transaction is not a valid contract.')

    @property
    def transaction_address(self) -> str:
        '''Returns transaction address.'''
        return self.tx_address or b2lx(self.tx.GetHash())

    @staticmethod
    def is_valid_contract_script(script_ops) -> bool:
        '''Checking if contract script is an Atomic Swap contract.'''
        try:
            is_valid = (
                script_ops[0] == script.OP_IF
                and script_ops[1] == script.OP_RIPEMD160
                and script_ops[3] == script_ops[15] == script.OP_EQUALVERIFY
                and script_ops[4] == script_ops[11] == script.OP_DUP
                and script_ops[5] == script_ops[12] == script.OP_HASH160
                and script_ops[7] == script.OP_ELSE
                and script_ops[9] == script.OP_CHECKLOCKTIMEVERIFY
                and script_ops[10] == script.OP_DROP
                and script_ops[14] == script.OP_ENDIF
                and script_ops[16] == script.OP_CHECKSIG
            )
        except IndexError:
            is_valid = False

        return is_valid

    def get_contract_utxo(self, wallet=None, secret: str=None, refund: bool=False, contract: str=None) -> Utxo:
        '''
        Creating UTXO object from contract.

        Args:
            wallet (obj): wallet object
            secret (str): tranaction secret (used to redeem contract)
            refund (bool): flag used for refund transactions
            contract (str): hex string with contract definition

        Returns:
            Utxo: Unspent transaction output object
        '''
        return Utxo(
            tx_id=self.transaction_address,
            vout=0,
            value=self.value,
            tx_script=self.vout.scriptPubKey.hex(),
            wallet=wallet,
            secret=secret,
            refund=refund,
            contract=contract,
        )

    def redeem(self, wallet, secret: str) -> BitcoinTransaction:
        '''
        Creates transaction that can redeem a contract.

        Args:
            wallet (obj): wallet object of the Atomic Swap contract recipient
            secret (str): transaction secret that should match the contract secret hash (after hashing)

        Returns:
            BitcoinTransaction: unsigned transaction object with redeem transaction

        Raises:
            ValueError: if contract balance is 0
        '''
        if self.balance == 0:
            raise ValueError("Balance of this contract is 0.")
        transaction = BitcoinTransaction(
            network=self.network,
            recipient_address=self.recipient_address,
            value=self.value,
            solvable_utxo=[self.get_contract_utxo(wallet, secret, contract=self.contract)]
        )
        transaction.create_unsigned_transaction()
        return transaction

    def refund(self, wallet):
        '''
        Creates transaction that can refund a contract.

        Args:
            wallet (obj): wallet object of the Atomic Swap contract creator

        Returns:
            BitcoinTransaction: unsigned transaction object with refund transaction

        Raises:
            RuntimeError: if contract is still valid
            ValueError: if contract balance is 0
        '''
        if self.locktime > datetime.utcnow():
            locktime_string = self.locktime.strftime('%Y-%m-%d %H:%M:%S')
            raise RuntimeError(f"This contract is still valid! It can't be refunded until {locktime_string} UTC.")
        if self.balance == 0:
            raise ValueError("Balance of this contract is 0.")
        transaction = BitcoinTransaction(
            network=self.network,
            recipient_address=self.refund_address,
            value=self.value,
            solvable_utxo=[self.get_contract_utxo(wallet, refund=True, contract=self.contract)],
            tx_locktime=self.locktime_timestamp,
        )
        transaction.create_unsigned_transaction()
        return transaction

    def participate(
        self,
        symbol: str,
        sender_address: str,
        recipient_address: str,
        value: float,
        utxo: list=None,
        token_address: str=None,
    ):
        '''
        Method for creating a second Atomic Swap transaction based on the secret hash from the current contract.

        Args:
            symbol (str): network symbol
            sender_address (str): wallet address of the transaction creator
            recipient_address (str): wallet address of the transaction recipient
            value (float): amount to be send
            utxo (list): list of UTXO objects. In None UTXO will be gathered automatically if needed
                (for bitcoin-based networks)
            token_address (str): address of the token contract if we want to use a token

        Returns:
            BitcoinAtomicSwapTransaction, EthereumAtomicSwapTransaction, None: Atomic Swap transaction object
                or None if something went wrong.
        '''
        network = self.network.get_network_by_symbol(symbol)
        if network.bitcoin_based:
            return network.atomic_swap(
                sender_address,
                recipient_address,
                value,
                utxo,
                self.secret_hash,
            )
        return network.atomic_swap(
            sender_address,
            recipient_address,
            str(value),
            self.secret_hash,
            token_address,
        )

    def show_details(self) -> dict:
        '''Returns a dictionary with transaction details.'''
        return {
            'contract_address': self.address,
            'confirmations': self.confirmations,
            'transaction_address': self.transaction_address,
            'transaction_link': self.network.get_transaction_url(self.transaction_address),
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.refund_address,
            'secret_hash': self.secret_hash,
            'value': self.value,
            'value_text': f'{self.value:.8f} {self.symbol}',
        }
