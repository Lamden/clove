from typing import Optional

from bitcoin.wallet import CBitcoinSecretError

from clove.network.bitcoin.base import BitcoinBaseNetwork
from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import auto_switch_params, from_base_units
from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class Monacoin(BitcoinBaseNetwork):
    """
    Class with all the necessary MONA network information based on
    https://github.com/monacoinproject/monacoin/blob/master-0.14/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'monacoin'
    symbols = ('MONA', )
    seeds = (
        'dnsseed.monacoin.org',
    )
    port = 9401
    message_start = b'\xfb\xc0\xb6\xdb'
    base58_prefixes = {
        'PUBKEY_ADDR': 50,
        'SCRIPT_ADDR': 5,
        'SECRET_KEY': 176
    }
    source_code_url = 'https://github.com/monacoinproject/monacoin/blob/master-0.14/src/chainparams.cpp'
    alternative_secret_key = 178

    @classmethod
    @auto_switch_params()
    def get_wallet(cls, *args, **kwargs):
        try:
            return super().get_wallet(*args, **kwargs)
        except CBitcoinSecretError:
            cls.base58_prefixes['SECRET_KEY'], cls.alternative_secret_key = \
                cls.alternative_secret_key, cls.base58_prefixes['SECRET_KEY']
            return super().get_wallet(*args, **kwargs)

    @property
    def latest_block(self):
        return clove_req_json('https://mona.chainseeker.info/api/v1/status')['blocks']

    @staticmethod
    def get_transaction(tx_address: str) -> dict:
        return clove_req_json(f'https://mona.chainseeker.info/api/v1/tx/{tx_address}')

    @classmethod
    def get_utxo(cls, address, amount):
        data = clove_req_json(f'https://mona.chainseeker.info/api/v1/utxos/{address}')
        unspent = sorted(data, key=lambda k: k['value'], reverse=True)

        utxo = []
        total = 0

        for output in unspent:
            value = from_base_units(output['value'])
            utxo.append(
                Utxo(
                    tx_id=output['txid'],
                    vout=output['vout'],
                    value=value,
                    tx_script=output['scriptPubKey']['hex'],
                )
            )
            total += value
            if total > amount:
                return utxo

        logger.debug(f'Cannot find enough UTXO\'s. Found %.8f from %.8f.', total, amount)

    @classmethod
    def extract_secret_from_redeem_transaction(cls, contract_address: str) -> Optional[str]:
        contract_transactions = clove_req_json(f'https://mona.chainseeker.info/api/v1/txids/{contract_address}')
        if len(contract_transactions) < 2:
            logger.debug('There is no redeem transaction on this contract yet.')
            return
        redeem_transaction = cls.get_transaction(contract_transactions[1])
        return cls.extract_secret(redeem_transaction['hex'])


class MonacoinTestNet(Monacoin):
    """
    Class with all the necessary MONA testing network information based on
    https://github.com/monacoinproject/monacoin/blob/master-0.14/src/chainparams.cpp
    (date of access: 01/18/2018)
    """
    name = 'test-monacoin'
    seeds = (
        'testnet-dnsseed.monacoin.org',
    )
    port = 19403
    message_start = b'\xfd\xd2\xc8\xf1'
    base58_prefixes = {
        'PUBKEY_ADDR': 111,
        'SCRIPT_ADDR': 196,
        'SECRET_KEY': 239
    }
    testnet = True

    @property
    def latest_block(self):
        raise NotImplementedError

    @staticmethod
    def get_transaction(tx_address: str) -> dict:
        raise NotImplementedError

    @classmethod
    def get_utxo(cls, address, amount):
        raise NotImplementedError

    @classmethod
    def extract_secret_from_redeem_transaction(cls, contract_address: str) -> Optional[str]:
        raise NotImplementedError
