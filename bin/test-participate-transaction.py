#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import (
    get_network, get_transaction_from_address, get_utxo, print_error, print_section, print_tx_address
)

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Redeem atomic swap transaction.")
    parser.add_argument('-tx', '--transaction', help='Contract transaction address', type=str, required=True)
    parser.add_argument('-r', '--recipient', help='Recipient address', type=str, required=True)
    parser.add_argument('-p', '--private-key', help='Private key', type=str, required=True)
    parser.add_argument('-n', '--network', help='Network for creating transaction in', type=str, required=True)
    parser.add_argument('-a', '--amount', help='Transaction amount', type=float, required=True)
    args = parser.parse_args()

    network = get_network(args.network)
    wallet = network.get_wallet(private_key=args.private_key)

    tx_hex = get_transaction_from_address(args.network, args.transaction)
    print_section('Found transaction:', tx_hex)

    print_section('Transaction audit...')
    contract = network.audit_contract(tx_hex)
    pprint(contract.show_details())

    utxo = get_utxo(args.network, wallet.get_address(), args.amount)
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
    print_tx_address(args.network, details["transaction_hash"])
