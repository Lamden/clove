#!/usr/bin/env python3

import importlib.util
import inspect
import os

from clove.network.bitcoin.base import BitcoinBaseNetwork

IGNORED = (
    '__init__.py',
    '__pycache__',
    '.coverage',
)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def get_networks(dir_name, base_class):
    base_class_name = base_class.__name__
    network_dir = os.path.join(BASE_DIR, f'clove/network/{dir_name}/')
    networks = sorted([file for file in os.listdir(network_dir) if file not in IGNORED])
    network_classes = []
    imports = []

    for filename in networks:
        spec = importlib.util.spec_from_file_location(
            'module.name',
            f'{network_dir}/{filename}'
        )
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        classes = []
        members = dir(module)
        assert base_class_name in members, f'Not importing {base_class_name}'
        for member in members:
            if member.startswith('__') or member == base_class_name:
                continue
            item = getattr(module, member)
            if inspect.isclass(item) and issubclass(item, base_class):
                classes.append(item)
        class_names = ', '.join([c.__name__ for c in classes])
        network_classes.append(class_names)
        imports.append(f'from clove.network.{dir_name}.{filename[:-3]} import {class_names}')
    return network_classes, imports


bitcoin_classes, bitcoin_imports = get_networks('bitcoin_based', BitcoinBaseNetwork)


print('from clove.network.bitcoin import Bitcoin, BitcoinTestNet')

for import_str in bitcoin_imports:
    print(import_str)

print('from clove.network.ethereum import Ethereum, EthereumTestnet')

print('\nBITCOIN_BASED = (')
print('    Bitcoin, BitcoinTestNet,')
for classes in bitcoin_classes:
    print(f'    {classes},')
print(')\n')

print('ETHEREUM_BASED = (')
print('    Ethereum, EthereumTestnet,')
print(')\n')

print('\n__all__ = BITCOIN_BASED + ETHEREUM_BASED')
