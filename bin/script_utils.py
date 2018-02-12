#!/usr/bin/env python3

import json
import random
from urllib.error import HTTPError, URLError
import urllib.request

from clove.network.bitcoin import Utxo
from clove.utils.bitcoin import satoshi_to_btc


def get_transaction_from_address(address):
    print('>>> Searching for transaction:', address)
    api_url = f'https://api.blockcypher.com/v1/btc/test3/txs/{address}?limit=50&includeHex=true'
    try:
        with urllib.request.urlopen(api_url) as url:
            if url.status != 200:
                return
            data = json.loads(url.read().decode())
            return data['hex']
    except (URLError, HTTPError):
        print('>>> Cannot find such transaction')
        exit()


def get_utxo(address, amount):
    print('>>> Searching for UTXO\'s')
    api_url = \
        f'https://api.blockcypher.com/v1/btc/test3/addrs/{address}/full?limit=50?unspentOnly=true&includeScript=true'
    utxo = []
    total = 0
    try:
        with urllib.request.urlopen(api_url) as url:
            if url.status != 200:
                return
            data = json.loads(url.read().decode())
            # try to use different transactions each time
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
            exit(f'>>> Cannot find enough UTXO\'s. {total:.8f} is all that you\'ve got.')
    except (URLError, HTTPError):
        print('>>> Cannot get UTXO\'s from API')
        return
