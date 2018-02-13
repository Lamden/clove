#!/usr/bin/env python3

import argparse
import os
from pprint import pprint
import sys

from script_utils import get_transaction_from_address

from clove.network import BitcoinTestNet

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Audit contract transaction.")
    parser.add_argument('-tx', '--transaction', help='Transaction address', type=str, required=True)

    args = parser.parse_args()

    btc_network = BitcoinTestNet()
    tx = get_transaction_from_address(args.transaction)
    contract = btc_network.audit_contract(tx)

    print('>>> Contract details:')
    pprint(contract.show_details())
