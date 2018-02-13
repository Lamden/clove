#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import get_transaction_from_address

from clove.network import BitcoinTestNet

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Refund contract transaction.")
    parser.add_argument('-tx', '--transaction', help='Transaction address', type=str, required=True)
    parser.add_argument('-p', '--private-key', help='Private key', type=str, required=True)

    args = parser.parse_args()

    btc_network = BitcoinTestNet()
    wallet = btc_network.get_wallet(private_key=args.private_key)
    tx = get_transaction_from_address(args.transaction)
    contract = btc_network.audit_contract(tx)

    print('>>> Contract details:')
    pprint(contract.show_details())

    refund_transaction = contract.refund(wallet)
    refund_transaction.add_fee_and_sign()

    print('>>> Refund transaction ready to be published')
    details = refund_transaction.show_details()
    pprint(details)

    publish = input('Do you want to publish this transaction (y/n): ')
    if publish != 'y':
        exit('>>> Bye!')

    print('>>> Publishing transaction')
    refund_transaction.publish()

    print('>>> Transaction published!')
    print(f'>>> https://live.blockcypher.com/btc-testnet/tx/{details["transaction_hash"]}/')
