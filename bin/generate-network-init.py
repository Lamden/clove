#!/usr/bin/env python3

import importlib.util
import inspect
import os

from clove.network.bitcoin import Bitcoin

IGNORED = (
    '__init__.py',
    '__pycache__',
)
networks = sorted([file for file in os.listdir('clove/network/bitcoin_based/') if file not in IGNORED])
bitcoin_classes = []

print('from clove.network.bitcoin import Bitcoin, BitcoinTestNet\n')

for filename in networks:
    spec = importlib.util.spec_from_file_location(
        'module.name',
        f'clove/network/bitcoin_based/{filename}'
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    classes = []
    members = dir(module)
    assert 'Bitcoin' in members, 'Not importing Bitcoin'
    for member in members:
        if member.startswith('__') or member == 'Bitcoin':
            continue
        item = getattr(module, member)
        if inspect.isclass(item) and issubclass(item, Bitcoin):
            classes.append(item)
    class_names = ', '.join([c.__name__ for c in classes])
    bitcoin_classes.append(class_names)
    print(f'from clove.network.bitcoin_based.{filename[:-3]} import {class_names}')

print('\n\nBITCOIN_BASES = [')
print('    Bitcoin, BitcoinTestNet,')
for classes in bitcoin_classes:
    print(f'    {classes},')
print(']')

print('__all__ = BITCOIN_BASES')
