#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import get_utxo

from clove.network import BitcoinTestNet

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

ALICE_ADDRESS = 'msJ2ucZ2NDhpVzsiNE5mGUFzqFDggjBVTM'
BOB_ADDRESS = 'mmJtKA92Mxqfi3XdyGReza69GjhkwAcBN1'
ALICE_PK = 'cSYq9JswNm79GUdyz6TiNKajRTiJEKgv4RxSWGthP3SmUHiX9WKe'


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate and publish atomic swap initial transaction.")
    parser.add_argument('-s', '--sender', help='Sender address', type=str, default=ALICE_ADDRESS)
    parser.add_argument('-r', '--recipient', help='Recipient address', type=str, default=BOB_ADDRESS)
    parser.add_argument('-a', '--amount', help='Transaction amount', type=float)
    parser.add_argument('-p', '--private-key', help='Private key', type=str, default=ALICE_PK)

    args = parser.parse_args()
    if not args.amount:
        args.amount = float(input('How many BTC do you want to transfer? ').replace(',', '.'))

    btc_network = BitcoinTestNet()

    print('>>> Creating transaction for BitcoinTestNet')
    print('>>> Sender address:\t', args.sender)
    print('>>> Recipient address:\t', args.recipient)
    print('>>> Transaction amount:\t', args.amount)

    wallet = btc_network.get_wallet(private_key=args.private_key)
    utxo = get_utxo(args.sender, args.amount)

    print(f'>>> Found {len(utxo)} UTXO\'s')
    pprint(utxo)
    transaction = btc_network.atomic_swap(args.sender, args.recipient, args.amount, utxo)

    print('>>> Adding fee and signing')
    transaction.add_fee_and_sign(wallet)

    print('>>> Transaction ready to be published')
    details = transaction.show_details()
    pprint(details)

    publish = input('Do you want to publish this transaction (y/n): ')
    if publish != 'y':
        print('>>> Bye!')
        exit()

    print('>>> Publishing transaction')
    transaction.publish()

    print('>>> Transaction published!')
    print(f'>>> https://live.blockcypher.com/btc-testnet/tx/{details["transaction_hash"]}/')
