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

    dead_networks = []

    for network in networks:
        print(network.name)
        if network.nodes:
            nodes = len(network.nodes)
            for node in network.nodes:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                result = sock.connect_ex((node, network.port))
                if result == 0:
                    print(Colors.OKGREEN, '', node, '✓', Colors.ENDC)
                else:
                    print(Colors.FAIL, '', node, '☠', Colors.ENDC)
                    nodes -= 1
            if not nodes:
                dead_networks.append(network)
        else:
            seeds = len(network.seeds)
            for seed in network.seeds:
                if hostname_resolves(seed):
                    print(Colors.OKGREEN, '', seed, '✓', Colors.ENDC)
                else:
                    print(Colors.FAIL, '', seed, '☠', Colors.ENDC)
                    seeds -= 1
            if not seeds:
                dead_networks.append(network)

    if dead_networks:
        print(Colors.FAIL, '\n\n☠ DEAD NETWORKS: ☠')
        for network in dead_networks:
            print('  ', network)
        print(Colors.ENDC)
