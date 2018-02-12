#!/usr/bin/env python3

import json
from urllib.error import HTTPError, URLError
import urllib.request


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
