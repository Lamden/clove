#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import get_transaction_from_address, print_error, print_section, print_tx_address

from clove.utils.search import get_network_by_symbol

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Refund contract transaction.")
    parser.add_argument('-tx', '--transaction', help='Transaction address', type=str, required=True)
    parser.add_argument('-c', '--contract', help='Contract', type=str, required=True)
    parser.add_argument('-p', '--private-key', help='Private key', type=str, required=True)
    parser.add_argument('-n', '--network', help='Network for creating transaction in', type=str, required=True)

    args = parser.parse_args()

    network = get_network_by_symbol(args.network)
    wallet = network.get_wallet(private_key=args.private_key)
    tx = get_transaction_from_address(args.network, args.transaction)
    contract = network.audit_contract(args.contract, tx)

    print_section('Contract details:')
    pprint(contract.show_details())

    refund_transaction = contract.refund(wallet)
    refund_transaction.add_fee_and_sign()

    print_section('Refund transaction ready to be published')
    details = refund_transaction.show_details()
    pprint(details)

    publish = input('Do you want to publish this transaction (y/n): ')
    if publish != 'y':
        exit('Bye!')

    print_section('Publishing transaction')
    if not refund_transaction.publish():
        print_error('Something went wrong, transaction was NOT published.')
        exit(1)

    print_section('Transaction published!')
    print_tx_address(args.network, details["transaction_address"])
