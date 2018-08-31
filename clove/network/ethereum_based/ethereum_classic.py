from eth_abi import encode_single
from web3 import HTTPProvider, Web3

from clove.constants import ETH_FILTER_MAX_ATTEMPTS
from clove.network.ethereum.base import EthereumBaseNetwork


class EthereumClassic(EthereumBaseNetwork):

    name = 'ethereum-classic'
    symbols = ('ETC',)
    web3_provider_address = 'https://web3.gastracker.io/'
    blockexplorer_tx = 'http://gastracker.io/tx/{0}'
    filtering_supported = True

    contract_address = '0x0ff1C3dD4b262a0324910A6E30CaA182204d9163'

    def find_transaction_details_in_redeem_event(self, recipient_address: str, secret_hash: str, block_number: int):
        # web3.gastracker.io node does not support filtering
        # etc-geth.0xinfra.com not is not stable so it is used only for filtering
        filterable_web3 = Web3(HTTPProvider('https://etc-geth.0xinfra.com/'))

        event_signature_hash = self.web3.sha3(text="RedeemSwap(address,bytes20,bytes32)").hex()
        filter_options = {
            'fromBlock': block_number,
            'address': self.contract_address,
            'topics': [
                event_signature_hash,
                '0x' + encode_single('address', recipient_address).hex(),
                '0x' + encode_single('bytes20', bytes.fromhex(secret_hash)).hex()
            ]
        }

        event_filter = filterable_web3.eth.filter(filter_options)

        for _ in range(ETH_FILTER_MAX_ATTEMPTS):
            events = event_filter.get_all_entries()
            if events:
                return {
                    'secret': events[0]['data'][2:],
                    'transaction_hash': events[0]['transactionHash'].hex()
                }
