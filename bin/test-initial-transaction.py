#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import print_error, print_section, print_tx_address

from clove.utils.search import get_network_by_symbol

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate and publish atomic swap initial transaction.")
    parser.add_argument('-n', '--network', help='Network for creating transaction in', type=str, required=True)
    parser.add_argument('-s', '--sender', help='Sender address', type=str, required=True)
    parser.add_argument('-r', '--recipient', help='Recipient address', type=str, required=True)
    parser.add_argument('-a', '--amount', help='Transaction amount', type=float, required=True)
    parser.add_argument('-p', '--private-key', help='Private key', type=str, required=True)
    args = parser.parse_args()

    network = get_network_by_symbol(args.network)

    print_section('Creating transaction for', args.network)
    print_section('Sender address:\t', args.sender)
    print_section('Recipient address:\t', args.recipient)
    print_section('Transaction amount:\t', args.amount)

    wallet = network.get_wallet(private_key=args.private_key)
    utxo = network.get_utxo(args.sender, args.amount)
    if not utxo:
        print_error('UTXO not found')
        exit(1)

    print_section(f'Found {len(utxo)} UTXO\'s')
    pprint(utxo)
    transaction = network.atomic_swap(args.sender, args.recipient, args.amount, utxo)

    print_section('Adding fee and signing')
    transaction.add_fee_and_sign(wallet)

    print_section('Transaction ready to be published')
    details = transaction.show_details()
    pprint(details)

    publish = input('Do you want to publish this transaction (y/n): ')
    if publish != 'y':
        print_section('Bye!')
        exit()

    print_section('Publishing transaction')
    if not transaction.publish():
        print_error('Something went wrong, transaction was NOT published.')
        exit(1)
    print_section('Transaction published!')
    print_tx_address(args.network, details["transaction_address"])
