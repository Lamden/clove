#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import get_transaction_from_address

from clove.network import BitcoinTestNet

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Redeem atomic swap transaction.")
    parser.add_argument('-tx', '--transaction', help='Contract transaction address', type=str, required=True)
    parser.add_argument('-p', '--private-key', help='Private key', type=str, required=True)
    parser.add_argument('-s', '--secret', help='Secret', type=str, required=True)
    args = parser.parse_args()

    btc_network = BitcoinTestNet()
    wallet = btc_network.get_wallet(private_key=args.private_key)

    tx_hex = get_transaction_from_address(args.transaction)
    print('>>> Found transaction:', tx_hex)

    print('>>> Transaction audit...')
    contract = btc_network.audit_contract(tx_hex)
    pprint(contract.show_details())

    print('>>> Creating redeem transaction using secret:', args.secret)
    redeem_transaction = contract.redeem(wallet, args.secret)

    print('>>> Adding fee and signing...')
    redeem_transaction.add_fee_and_sign()

    print('>>> Transaction ready to be published')
    details = redeem_transaction.show_details()
    pprint(details)

    publish = input('Do you want to publish this transaction (y/n): ')
    if publish != 'y':
        exit('>>> Bye!')

    print('>>> Publishing transaction')
    redeem_transaction.publish()

    print('>>> Transaction published!')
    print(f'>>> https://live.blockcypher.com/btc-testnet/tx/{details["transaction_hash"]}/')
