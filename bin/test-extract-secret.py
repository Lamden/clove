#!/usr/bin/env python3

import argparse
import os
import sys

from script_utils import print_section

from clove.utils.search import get_network_by_symbol

sys.path.append(os.path.dirname(os.path.realpath(__file__)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Extract secret from transaction.")
    parser.add_argument('-c', '--contract-address', help='Contract address', type=str, required=True)
    parser.add_argument('-n', '--network', help='Transaction network', type=str, required=True)
    parser.add_argument('-k', '--cryptoid-api-key', help='Cryptoid API Key', type=str, required=False)

    args = parser.parse_args()

    network = get_network_by_symbol(args.network)
    if args.cryptoid_api_key:
        os.environ['CRYPTOID_API_KEY'] = args.cryptoid_api_key
    secret = network.extract_secret_from_redeem_transaction(args.contract_address)

    print_section('Secret:', secret)
