#!/usr/bin/env python3

import socket

from clove.network import __all__ as networks


class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def hostname_resolves(hostname):
    try:
        socket.gethostbyname_ex(hostname)
        return True
    except socket.error:
        return False


if __name__ == '__main__':

    for network in networks:
        print(network.name)
        for seed in network.seeds:
            if hostname_resolves(seed):
                print(Colors.OKGREEN, '', seed, '✓', Colors.ENDC)
            else:
                print(Colors.FAIL, '', seed, '☠', Colors.ENDC)
