#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import get_transaction_from_address, print_section

from clove.network import BitcoinTestNet

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Audit contract transaction.")
    parser.add_argument('-tx', '--transaction', help='Transaction address', type=str, required=True)
    parser.add_argument('-c', '--contract', help='Contract', type=str, required=True)
    parser.add_argument('-n', '--network', help='Network for creating transaction in', type=str, required=True)

    args = parser.parse_args()

    btc_network = BitcoinTestNet()
    tx = get_transaction_from_address(args.network, args.transaction)
    contract = btc_network.audit_contract(args.contract, tx)

    print_section('Contract details:')
    pprint(contract.show_details())
