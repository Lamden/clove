#!/usr/bin/env python3

import argparse
import os
import sys

from script_utils import get_network, get_transaction_from_address, print_section

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Extract secret from transaction.")
    parser.add_argument('-tx', '--transaction', help='Transaction address', type=str, required=True)
    parser.add_argument('-n', '--network', help='Transaction network', type=str, required=True)

    args = parser.parse_args()

    tx = get_transaction_from_address(args.network, args.transaction)

    network = get_network(args.network)
    secret = network.extract_secret(tx)

    print_section('Secret:', secret)
