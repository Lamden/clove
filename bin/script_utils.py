#!/usr/bin/env python3

import json
from urllib.error import HTTPError, URLError
import urllib.request

from colorama import Fore, Style

from clove.network.base import BaseNetwork
from clove.network.bitcoin import BitcoinTestNet


def print_section(*args):
    print(Fore.GREEN, '▶', ' '.join(map(str, args)), Style.RESET_ALL)


def print_error(*args):
    print(Fore.RED, '●', ' '.join(map(str, args)), Style.RESET_ALL)


def get_network(symbol):
    testnet = symbol.endswith('_TESTNET')
    if testnet:
        symbol = symbol.replace('_TESTNET', '')
        return BitcoinTestNet.get_network_class_by_symbol(symbol)()
    return BaseNetwork.get_network_class_by_symbol(symbol)()


def api_network_symbol(symbol):
    SYMBOL_API_MAP = {
        'BTC': 'btc/main',
        'BTC_TESTNET': 'btc/test3',
        'LTC': 'ltc/main',
        'DOGE': 'doge/main',
        'DASH': 'dash/main',
    }
    return SYMBOL_API_MAP[symbol]


def print_tx_address(symbol, tx):
    symbol_url = symbol.lower().replace('_', '-')
    print(f'https://live.blockcypher.com/{symbol_url}/tx/{tx}/')


def get_transaction_from_address(network, address):
    print_section('Searching for transaction:', address)
    api_network = api_network_symbol(network)
    api_url = f'https://api.blockcypher.com/v1/{api_network}/txs/{address}?limit=50&includeHex=true'
    try:
        with urllib.request.urlopen(api_url) as url:
            if url.status != 200:
                return
            data = json.loads(url.read().decode())
            return data['hex']
    except (URLError, HTTPError):
        print_section('Cannot find such transaction')
        exit(1)
