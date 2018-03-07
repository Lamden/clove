from bitcoin.core import CMutableTxIn, COutPoint, lx, script, x


class Utxo(object):

    def __init__(self, tx_id, vout, value, tx_script, wallet=None, secret=None, refund=False, contract=None):
        self.tx_id = tx_id
        self.vout = vout
        self.value = value
        self.tx_script = tx_script
        self.wallet = wallet
        self.secret = secret
        self.refund = refund
        self.contract = contract

    @property
    def outpoint(self):
        return COutPoint(lx(self.tx_id), self.vout)

    @property
    def tx_in(self):
        return CMutableTxIn(self.outpoint, scriptSig=script.CScript(self.unsigned_script_sig), nSequence=0)

    @property
    def parsed_script(self):
        return script.CScript.fromhex(self.tx_script)

    @property
    def unsigned_script_sig(self):
        if self.contract:
            if self.refund:
                return [script.OP_FALSE, x(self.contract)]
            elif self.secret:
                return [x(self.secret), script.OP_TRUE, x(self.contract)]
        return []

    def __repr__(self):
        return "Utxo(tx_id='{}', vout='{}', value='{}', tx_script='{}', wallet={}, secret={}, refund={})".format(
            self.tx_id,
            self.vout,
            self.value,
            self.tx_script,
            self.wallet,
            str(self.secret),
            self.refund,
        )
