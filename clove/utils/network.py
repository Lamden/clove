import socket


def hostname_resolves(hostname):
    try:
        socket.gethostbyname_ex(hostname)
        return True
    except socket.error:
        return False
