#!/usr/bin/env python3

import glob
import os
import re
from urllib.error import HTTPError, URLError
import urllib.request

base_pattern = (
    '{message_start}\[0\] = (.*?);.*?'
    '{message_start}\[1\] = (.*?);.*?'
    '{message_start}\[2\] = (.*?);.*?'
    '{message_start}\[3\] = (.*?);.*?'
    'base58Prefixes\[PUBKEY_ADDRESS\]\s*= (.*?);.*?'
    'base58Prefixes\[SCRIPT_ADDRESS\]\s*= (.*?);.*?'
    'base58Prefixes\[SECRET_KEY\]\s* = (.*?);'
)
message_start_params = ('pchMessageStart', 'netMagic')

chainparams_patterns = [
    re.compile('CMainParams.*?' + base_pattern.format(message_start=message_start), re.S)
    for message_start in message_start_params
]
chainparams_test_patterns = [
    re.compile('CTestNetParams.*?' + base_pattern.format(message_start=message_start), re.S)
    for message_start in message_start_params
]

main_message_start_pattern = re.compile('pchMessageStart\[4\] = {(.*?),(.*?),(.*?),(.*?)};', re.S)
main_message_start_test_pattern = re.compile(
    'if \(fTestNet\).*?'
    'pchMessageStart\[0\] = (.*?);.*?'
    'pchMessageStart\[1\] = (.*?);.*?'
    'pchMessageStart\[2\] = (.*?);.*?'
    'pchMessageStart\[3\] = (.*?);.*?',
    re.S
)
base58_pattern = re.compile(
    'class CBitcoinAddress.*?'
    'PUBKEY_ADDRESS = (.*?),.*?'
    'SCRIPT_ADDRESS = (.*?),',
    re.S
)
base58_test_pattern = re.compile(
    'class CBitcoinAddress.*?'
    'PUBKEY_ADDRESS_TEST = (.*?),.*?'
    'SCRIPT_ADDRESS_TEST = (.*?),',
    re.S
)


def add_param_lines(lines, index, testnet=False):
    result = set_params(lines, index, testnet)
    return result if result else lines


def set_params(lines, index, testnet=False):
    message_start = None
    base58_prefixes = None

    github_line_offset = next((i for i, line in enumerate(lines[index:]) if 'github.com' in line), None)
    port_line_offset = next((i for i, line in enumerate(lines[index:]) if 'port =' in line), None)

    if github_line_offset is None or port_line_offset is None:
        return

    port_line_index = index + port_line_offset
    port_line = lines[port_line_index]
    github_line = lines[index + github_line_offset]

    if len(lines) == port_line_index + 1 or not lines[port_line_index + 1].strip():
        github_link = create_github_link(github_line)
        if 'chainparams.cpp' in github_link:
            with urllib.request.urlopen(github_link) as url:
                if url.status != 200:
                    return
                data = url.read().decode()

                message_start, base58_prefixes = find_params_in_chainparams_file(data, testnet=testnet)

        elif 'net.cpp' in github_link:
            main_github_link = github_link.replace('net.cpp', 'main.cpp')
            with urllib.request.urlopen(main_github_link) as url:
                if url.status != 200:
                    return
                data = url.read().decode()
                message_start = find_message_start_in_main_file(data, testnet=testnet)

            base58_github_link = github_link.replace('net.cpp', 'base58.h')
            with urllib.request.urlopen(base58_github_link) as url:
                if url.status != 200:
                    return
                data = url.read().decode()
                base58_prefixes = find_base58_prefixes_in_base58_file(data, testnet=testnet)

        if not message_start or not base58_prefixes:
            return

        indent = len(port_line) - len(port_line.lstrip(' '))
        param_lines = [indent * ' ' + line + '\n' for line in [message_start] + base58_prefixes]
        return lines[:port_line_index + 1] + param_lines + lines[port_line_index + 1:]


def create_github_link(line):
    github_base = 'https://raw.githubusercontent.com/'

    github_link = line.strip().split('github.com/')[1]
    github_link = github_link.replace('/blob/', '/')

    return github_base + github_link


def find_message_start_in_main_file(data, testnet=False):
    if testnet:
        search = main_message_start_test_pattern.search(data)
    else:
        search = main_message_start_pattern.search(data)

    if search:
        strings = [s.strip() for s in search.groups()]
        return extract_message_start(strings)


def find_base58_prefixes_in_base58_file(data, testnet=False):
    if testnet:
        search = base58_test_pattern.search(data)
    else:
        search = base58_pattern.search(data)

    if search:
        strings = [s.strip() for s in search.groups()]
        try:
            values = list(map(int, strings))
            values.append(values[0] + 128)
            return get_prefixes_lines(values)
        except ValueError:
            return


def find_params_in_chainparams_file(data, testnet=False):
    message_start = None
    base58_prefixes = None
    search = None

    if testnet:
        for pattern in chainparams_test_patterns:
            search = pattern.search(data)
            if search:
                break
    else:
        for pattern in chainparams_patterns:
            search = pattern.search(data)
            if search:
                break

    if search:
        results = search.groups()
        message_start = extract_message_start(results[:4])
        base58_prefixes = extract_base58_prefixes(results[4:])

    return message_start, base58_prefixes


def extract_message_start(strings):
    message = ''.join(strings).replace('0x', '\\x')
    return f"message_start = b'{message}'"


def extract_base58_prefixes(strings):
    prefixes = list(strings)

    if '(' in strings[0]:
        prefixes = [extract_from_brackets(s) for s in strings]
    elif '{' in strings[0]:
        prefixes = [extract_from_curly_brackets(s) for s in strings]

    for i, prefix in enumerate(prefixes):
        try:
            if isinstance(prefix, str):
                if '+' in prefix:
                    values = prefix.split('+')
                    prefix = sum(map(int, values))
                elif '0x' in prefix:
                    prefix = int(prefix, 16)
            prefixes[i] = prefix
            int(prefix)
        except ValueError:
            return

    return get_prefixes_lines(prefixes)


def get_prefixes_lines(prefixes):
    return [
        "base58_prefixes = {",
        f"    'PUBKEY_ADDR': {prefixes[0]},",
        f"    'SCRIPT_ADDR': {prefixes[1]},",
        f"    'SECRET_KEY': {prefixes[2]}",
        "}"
    ]


def extract_from_brackets(line):
    result = re.search('\((.*?)\)', line)
    if result:
        content = result.group(1)
        prefix = content.split(',')[-1]
        prefix = prefix.strip(' ()')
        return prefix


def extract_from_curly_brackets(line):
    result = re.search('{(.*?)}', line)
    if result:
        prefix = result.group(1)
        return prefix


if __name__ == '__main__':
    base_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    network_dir = os.path.join(base_dir, 'clove/network/bitcoin_based/')
    files = sorted(glob.glob(network_dir+'*'))
    for file_path in files:
        if not os.path.isfile(file_path):
            continue

        filename = os.path.basename(file_path)
        with open(file_path, 'r') as f:
            file_lines = f.readlines()
            file_length = len(file_lines)

            indices = [i for i, line in enumerate(file_lines) if 'Class with all the necessary' in line]
            if not indices:
                continue
            try:
                if len(indices) == 2:
                    file_lines = add_param_lines(file_lines, indices[1], testnet=True)

                file_lines = add_param_lines(file_lines, indices[0])
            except(HTTPError, URLError):
                continue

            if len(file_lines) == file_length:
                continue

        with open(file_path, 'w') as f:
            f.writelines(file_lines)
            print(f'Added params to {filename}')
