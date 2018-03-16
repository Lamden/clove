#!/usr/bin/env python3

from colorama import Fore, Style

from clove.utils.external_source import get_transaction
from clove.utils.search import get_network_object


def print_section(*args):
    print(Fore.GREEN, '▶', ' '.join(map(str, args)), Style.RESET_ALL)


def print_error(*args):
    print(Fore.RED, '●', ' '.join(map(str, args)), Style.RESET_ALL)


def get_network(symbol):
    testnet = symbol.endswith('-TESTNET')
    if testnet:
        symbol = symbol[:-8]
    return get_network_object(symbol, testnet)


def print_tx_address(symbol, tx):
    symbol_url = symbol.lower().replace('_', '-')
    print(f'https://live.blockcypher.com/{symbol_url}/tx/{tx}/')


def get_transaction_from_address(symbol, address):
    print_section('Searching for transaction:', address)
    network = get_network(symbol)
    tx = get_transaction(network.default_symbol, address, network.is_test_network())
    if not tx:
        print_section('Cannot find such transaction')
        exit(1)
    return tx['hex']
