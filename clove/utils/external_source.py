import json
from urllib.error import HTTPError, URLError
import urllib.request

from clove.utils.logging import logger


def get_last_transactions(network: str) -> list:

    req = urllib.request.Request(
        f'https://chainz.cryptoid.info/{network}/api.dws?q=lasttxs',
        headers={
            'User-Agent': 'Clove'
        })
    try:
        resp = urllib.request.urlopen(req)
    except (HTTPError, URLError) as e:
        logger.debug('Could not get last transactions for %s network', network)
        logger.exception(e)
        return

    if resp.status != 200:
        logger.debug(
            'Could not get last transactions for %s network, status code: %s',
            network, resp.status)
        return

    return [t['hash'] for t in json.loads(resp.read().decode())]


def get_transaction_size(network: str, tx_hash: str) -> int:
    """WARNING: this method is using undocumented endpoint used by chainz.cryptoid.info site."""
    req = urllib.request.Request(
        f'https://chainz.cryptoid.info/explorer/tx.raw.dws?coin={network}&id={tx_hash}',
        headers={
            'User-Agent': 'Clove'
        })
    try:
        resp = urllib.request.urlopen(req)
    except (HTTPError, URLError) as e:
        logger.debug('Could not get transaction %s size for %s network',
                     tx_hash, network)
        logger.debug(e)
        return
    tx_details = json.loads(resp.read().decode())
    return tx_details['size']


def get_transaction_fee(network: str, tx_hash: str) -> float:
    req = urllib.request.Request(
        f'https://chainz.cryptoid.info/{network}/api.dws?q=txinfo&t={tx_hash}',
        headers={
            'User-Agent': 'Clove'
        })
    try:
        resp = urllib.request.urlopen(req)
    except (HTTPError, URLError) as e:
        logger.debug('Could not get transaction %s fee for %s network',
                     tx_hash, network)
        logger.debug(e)
        return
    tx_details = json.loads(resp.read().decode())
    return tx_details['fees']
