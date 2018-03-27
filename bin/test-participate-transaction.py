#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import get_transaction_from_address, print_error, print_section, print_tx_address

from clove.utils.search import get_network_by_symbol

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Creating participate transaction.")
    parser.add_argument('-tx', '--transaction', help='Contract transaction address', type=str, required=True)
    parser.add_argument('-c', '--contract', help='Contract', type=str, required=True)
    parser.add_argument('-r', '--recipient', help='Recipient address', type=str, required=True)
    parser.add_argument('-p', '--private-key', help='Private key', type=str, required=True)
    parser.add_argument(
        '-in', '--initial-network', help='Initial transaction network', type=str, required=True
    )
    parser.add_argument('-n', '--network', help='Network for creating transaction in', type=str, required=True)
    parser.add_argument('-a', '--amount', help='Transaction amount', type=float, required=True)
    args = parser.parse_args()

    network = get_network_by_symbol(args.network)
    wallet = network.get_wallet(private_key=args.private_key)

    tx_hex = get_transaction_from_address(args.initial_network, args.transaction)
    print_section('Found transaction:', tx_hex)

    print_section('Transaction audit...')
    contract = network.audit_contract(args.contract, tx_hex)
    pprint(contract.show_details())

    utxo = network.get_utxo(wallet.address, args.amount)
    if not utxo:
        print_error('UTXO not found')
        exit(1)
    print_section(f'Found {len(utxo)} UTXO\'s')
    pprint(utxo)

    participate_transaction = contract.participate(
        args.network.replace('_TESTNET', '').lower(),
        wallet.address,
        args.recipient,
        args.amount,
        utxo
    )

    print_section('Adding fee and signing...')
    participate_transaction.add_fee_and_sign(wallet)

    print_section('Transaction ready to be published')
    details = participate_transaction.show_details()
    pprint(details)

    publish = input('Do you want to publish this transaction (y/n): ')
    if publish != 'y':
        print_section('Bye!')
        exit()

    print_section('Publishing transaction')
    if not participate_transaction.publish():
        print_error('Something went wrong, transaction was NOT published.')
        exit(1)

    print_section('Transaction published!')
    print_tx_address(args.network, details["transaction_address"])
