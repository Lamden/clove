#!/usr/bin/env python3

import socket

from clove.network import __all__ as networks


class Colors:
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def hostname_resolves(hostname):
    try:
        response = socket.gethostbyname_ex(hostname)
        return response[2]
    except socket.error:
        return False


def check_node(node, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    return sock.connect_ex((node, port))


if __name__ == '__main__':

    dead_networks = []

    for network in networks:
        print(network.name)
        if network.nodes:
            nodes = len(network.nodes)
            for node in network.nodes:
                result = check_node(node, network.port)
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

                nodes = hostname_resolves(seed)
                nodes_counter = 0
                if not nodes:
                    print(Colors.FAIL, '', seed, '☠', Colors.ENDC)
                    continue
                print(Colors.OKGREEN, '', seed, Colors.ENDC)
                nodes_counter = len(nodes)
                for node in nodes:
                    result = check_node(node, network.port)
                    if result == 0:
                        print(Colors.OKGREEN, '   ', node, '✓', Colors.ENDC)
                    else:
                        print(Colors.FAIL, '   ', node, '☠', Colors.ENDC)
                        nodes_counter -= 1
                if not nodes_counter:
                    dead_networks.append(network)

    if dead_networks:
        print(Colors.FAIL, '\n\n☠ DEAD NETWORKS: ☠')
        for network in dead_networks:
            print('  ', network)
        print(Colors.ENDC)
