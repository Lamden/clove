from http.client import HTTPResponse
import json
import time
from typing import Optional
from urllib.error import HTTPError, URLError
import urllib.request

from clove.utils.logging import logger


def clove_req(url: str) -> Optional[HTTPResponse]:
    """Make a request with Clove user-agent header"""
    req = urllib.request.Request(url, headers={'User-Agent': 'Clove'})
    try:
        request_start = time.time()
        logger.debug('  Requesting: %s', url)
        resp = urllib.request.urlopen(req)
        response_time = time.time() - request_start
        logger.debug('Got response: %s [%.2fs]', url, response_time)
    except (HTTPError, URLError) as e:
        logger.warning('Could not open url %s', url)
        logger.exception(e)
        return
    return resp


def clove_req_json(url: str):
    """Make a request with Clove user-agent header and return json response"""
    resp = clove_req(url)
    if not resp or resp.status != 200:
        return

    return json.loads(resp.read().decode())
