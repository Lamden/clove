from http.client import HTTPResponse
import json
from typing import Optional
from urllib.error import HTTPError, URLError
import urllib.request

from clove.utils.logging import logger


def clove_req(url: str) -> Optional[HTTPResponse]:
    """Make a request with Clove user-agent header"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Clove'})
    try:
        resp = urllib.request.urlopen(req)
    except (HTTPError, URLError) as e:
        logger.debug('Could not open url %s', url)
        logger.exception(e)
        return
    return resp


def get_last_transactions(network: str) -> Optional[list]:

    resp = clove_req(f'https://chainz.cryptoid.info/{network}/api.dws?q=lasttxs')
    if not resp or resp.status != 200:
        logger.debug('Could not get last transactions for %s network', network)
        return
    return [t['hash'] for t in json.loads(resp.read().decode())]


def get_transaction_size(network: str, tx_hash: str) -> Optional[int]:
    """WARNING: this method is using undocumented endpoint used by chainz.cryptoid.info site."""
    resp = clove_req(f'https://chainz.cryptoid.info/explorer/tx.raw.dws?coin={network}&id={tx_hash}')
    if not resp or resp.status != 200:
        logger.debug('Could not get transaction %s size for %s network', tx_hash, network)
        return
    tx_details = json.loads(resp.read().decode())
    return tx_details['size']


def get_transaction_fee(network: str, tx_hash: str) -> Optional[float]:
    resp = clove_req(f'https://chainz.cryptoid.info/{network}/api.dws?q=txinfo&t={tx_hash}')
    if not resp or resp.status != 200:
        logger.debug('Could not get transaction %s fee for %s network', tx_hash, network)
        return
    tx_details = json.loads(resp.read().decode())
    return tx_details['fees']
