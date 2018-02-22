#!/usr/bin/env python3

import json
import random
import time
from urllib.error import HTTPError, URLError
import urllib.request

from colorama import Fore, Style

from clove.network.base import BaseNetwork
from clove.network.bitcoin import BitcoinTestNet, Utxo
from clove.utils.bitcoin import satoshi_to_btc


def print_section(*args):
    print(Fore.GREEN, '▶', ' '.join(map(str, args)), Style.RESET_ALL)


def print_error(*args):
    print(Fore.RED, '●', ' '.join(map(str, args)), Style.RESET_ALL)


def get_network(symbol):
    if symbol not in ('BTC', 'BTC_TESTNET', 'LTC', 'DOGE', 'DASH'):
        print_error(symbol, 'network in unsupported')
        exit(1)
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


def get_utxo(network, address, amount, api_url=None):
    api_network = api_network_symbol(network)
    api_url = api_url or \
        f'https://api.blockcypher.com/v1/{api_network}/addrs/{address}/'\
        'full?limit=20&unspentOnly=true&includeScript=true'
    if 'outstart' in api_url:
        page = round(int(api_url.split('outstart=')[1].split('&')[0]) / 20) + 1
        print_section(f'Searching for UTXO\'s on page {page}')
    else:
        print_section('Searching for UTXO\'s')
    utxo = []
    total = 0
    try:
        with urllib.request.urlopen(api_url) as url:
            if url.status != 200:
                return
            data = json.loads(url.read().decode())
            # try to use different transactions each time
            if 'txs' not in data:
                # hack for pagination support
                data['txs'] = [data, ]
            random.shuffle(data['txs'])
            for txs in data['txs']:
                for i, output in enumerate(txs['outputs']):
                    if not output['addresses'] or output['addresses'][0] != address \
                            or output['script_type'] != 'pay-to-pubkey-hash' or 'spent_by' in output:
                        continue
                    value = satoshi_to_btc(output['value'])
                    utxo.append(
                        Utxo(
                            tx_id=txs['hash'],
                            vout=i,
                            value=value,
                            tx_script=output['script'],
                        )
                    )
                    total += value
                    if total > amount:
                        return utxo
            if data['txs'][0]['next_outputs']:
                time.sleep(0.5)
                return get_utxo(network, address, amount, data['txs'][0]['next_outputs'])
            print_error(f'Cannot find enough UTXO\'s. {total:.8f} is all that you\'ve got.')
            exit(1)
    except (URLError, HTTPError) as e:
        print_error(f'Cannot get UTXO\'s from API {e}')
        exit(1)
