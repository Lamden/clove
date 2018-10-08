import time

import requests

from clove.exceptions import ExternalApiRequestLimitExceeded
from clove.utils.logging import logger


def clove_req_json(url: str):
    """
    Make a request with Clove user-agent header and return json response

    Args:
        url (str): url to get data from

    Returns:
        dict: response data

    Raises:
        ExternalApiRequestLimitExceeded: if response status code is 429

    Example:
        >>> from clove.utils.external_source import clove_req_json
        >>> clove_req_json('https://testnet.blockexplorer.com/api/status?q=getInfo')
        {'info': {
             'blocks': 1414831,
             'connections': 23,
             'difficulty': 1,
             'errors': 'Warning: unknown new rules activated (versionbit 28)',
             'network': 'testnet',
             'protocolversion': 70012,
             'proxy': '',
             'relayfee': 1e-05,
             'testnet': True,
             'timeoffset': 0,
             'version': 120100}}
    """

    logger.debug('  Requesting: %s', url)
    request_start = time.time()
    resp = requests.get(url, headers={'User-Agent': 'Clove'})

    response_time = time.time() - request_start
    logger.debug('Got response: %s [%.2fs]', url, response_time)

    if resp.status_code == 429:
        logger.error(f'Requests limit exceeded when requesting url: {url}')
        raise ExternalApiRequestLimitExceeded(f'url: {url}')

    if resp.status_code != 200:
        logger.error(f'Unexpected status code when requesting url: {url}')
        return

    return resp.json()
