from datetime import datetime

from bitcoin.core import b2lx, b2x, script
from bitcoin.wallet import CBitcoinAddress, P2PKHBitcoinAddress

from clove.network.bitcoin.transaction import BitcoinTransaction
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import auto_switch_params, deserialize_raw_transaction, from_base_units


class BitcoinContract(object):

    @auto_switch_params(1)
    def __init__(self, network, contract: str, raw_transaction: str):
        self.network = network
        self.symbol = self.network.default_symbol
        self.contract = contract
        self.tx = deserialize_raw_transaction(raw_transaction)

        if not self.tx.vout:
            raise ValueError('Given transaction has no outputs.')

        contract_tx_out = self.tx.vout[0]
        contract_script = script.CScript.fromhex(self.contract)
        script_pub_key = contract_script.to_p2sh_scriptPubKey()
        valid_p2sh = script_pub_key == contract_tx_out.scriptPubKey
        self.address = str(CBitcoinAddress.from_scriptPubKey(script_pub_key))

        script_ops = list(contract_script)
        if valid_p2sh and self.is_valid_contract_script(script_ops):
            self.recipient_address = str(P2PKHBitcoinAddress.from_bytes(script_ops[6]))
            self.refund_address = str(P2PKHBitcoinAddress.from_bytes(script_ops[13]))
            self.locktime_timestamp = int.from_bytes(script_ops[8], byteorder='little')
            self.locktime = datetime.fromtimestamp(self.locktime_timestamp)
            self.secret_hash = b2x(script_ops[2])
            self.value = from_base_units(contract_tx_out.nValue)
        else:
            raise ValueError('Given transaction is not a valid contract.')

    @property
    def transaction_address(self):
        return b2lx(self.tx.GetHash())

    @staticmethod
    def is_valid_contract_script(script_ops):
        try:
            is_valid = (
                script_ops[0] == script.OP_IF
                and script_ops[1] == script.OP_SHA256
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

    def get_contract_utxo(self, wallet=None, secret=None, refund=False, contract=None):
        return Utxo(
            tx_id=self.transaction_address,
            vout=0,
            value=self.value,
            tx_script=self.tx.vout[0].scriptPubKey.hex(),
            wallet=wallet,
            secret=secret,
            refund=refund,
            contract=contract,
        )

    def redeem(self, wallet, secret):
        transaction = BitcoinTransaction(
            network=self.network,
            recipient_address=self.recipient_address,
            value=self.value,
            solvable_utxo=[self.get_contract_utxo(wallet, secret, contract=self.contract)]
        )
        transaction.create_unsigned_transaction()
        return transaction

    def refund(self, wallet):
        if self.locktime > datetime.utcnow():
            locktime_string = self.locktime.strftime('%Y-%m-%d %H:%M:%S')
            raise RuntimeError(f"This contract is still valid! It can't be refunded until {locktime_string}.")
        transaction = BitcoinTransaction(
            network=self.network,
            recipient_address=self.refund_address,
            value=self.value,
            solvable_utxo=[self.get_contract_utxo(wallet, refund=True, contract=self.contract)],
            tx_locktime=self.locktime_timestamp,
        )
        transaction.create_unsigned_transaction()
        return transaction

    def participate(self, symbol, sender_address, recipient_address, value, utxo):
        network_class = self.network.get_network_class_by_symbol(symbol)

        network = network_class()
        return network.atomic_swap(
            sender_address,
            recipient_address,
            value,
            utxo,
            self.secret_hash
        )

    def show_details(self):
        return {
            'contract_address': self.address,
            'transaction_address': self.transaction_address,
            'locktime': self.locktime,
            'recipient_address': self.recipient_address,
            'refund_address': self.refund_address,
            'secret_hash': self.secret_hash,
            'value': self.value,
            'value_text': f'{self.value:.8f} {self.symbol}',
        }
