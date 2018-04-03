#!/usr/bin/env python3

import argparse
from collections import namedtuple
from operator import attrgetter
import os

from pyquery import PyQuery as pq
import requests
from web3 import Web3

from script_utils import print_error, print_section

Token = namedtuple('Token', 'name, symbol, address')


class EthereumNetworkGenerator(object):

    # Most popular user agent based on http://www.browser-info.net/useragents
    USER_AGENT = 'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; FSL 7.0.6.01001)'

    def __init__(self, network='mainnet'):
        self.network = network
        self.tokens = []
        self.html = None
        self.ignored = []
        self.symbols = set()
        self.names = set()
        self.current_page = 1
        self.last_page = 999

    def get_pagination(self):
        pagination = self.html.find('#ContentPlaceHolder1_divpagingpanel p span').text().split()
        self.current_page = int(pagination[1])
        self.last_page = int(pagination[3])

    def extract_tokens(self):
        links = [l for l in self.html.find('#ContentPlaceHolder1_divresult tbody tr h5 a')]
        for l in links:
            address = l.attrib['href'].replace('/token/', '')
            name, symbol = l.text[:-1].split(' (')
            token = Token(name, symbol, Web3.toChecksumAddress(address))
            if symbol in self.symbols:
                print_error(f'Duplicate symbol {symbol} for token {name}. Ignoring.')
                self.ignored.append(token)
                continue
            elif name in self.names:
                print_error(f'Duplicate name {name} for token {symbol}. Ignoring.')
                self.ignored.append(token)
                continue
            self.tokens.append(token)
            self.symbols.add(symbol)
            self.names.add(name)
        print_section(f'Tokens counter: {len(self.tokens)}.')

    def scrap_tokens(self):

        while self.current_page <= self.last_page:
            headers = {'User-Agent': self.USER_AGENT}
            print_section(f'Scrapping page: {self.current_page} / {self.last_page}')
            response = requests.get(f'https://etherscan.io/tokens?p={self.current_page}', headers=headers)
            if response.status_code != 200:
                raise RuntimeError(f'Incorrect status code from etherscan: {response.status_code}')
            self.html = pq(response.content)
            self.get_pagination()
            self.extract_tokens()
            self.current_page += 1

        if self.ignored:
            print_error(f'Ignored {len(self.ignored)} tokens.')

    def save_tokens(self):

        sorted_tokens = sorted(self.tokens, key=attrgetter('name'))
        base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        tokens_file = os.path.join(base_dir, 'clove/network/ethereum_based/mainnet_tokens.py')

        f = open(tokens_file, 'w')
        f.write('''from clove.network.ethereum_based import Token

tokens = (
''')
        for token in sorted_tokens:
            f.write(f"    Token('{token.name}', '{token.symbol}', '{token.address}'),\n")
        f.write(')\n')
        f.close()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Audit contract transaction.")
    args = parser.parse_args()

    network_generator = EthereumNetworkGenerator()
    network_generator.scrap_tokens()

    publish = input('Create files with new tokens (y/n): ')
    if publish != 'y':
        print_section('Bye!')
        exit()

    network_generator.save_tokens()
