from datetime import datetime
from http.client import HTTPResponse
import json
import os
from typing import Optional
from urllib.error import HTTPError, URLError
import urllib.request

from bitcoin.core import COIN

from clove.network.bitcoin.utxo import Utxo
from clove.utils.bitcoin import satoshi_to_btc
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


def clove_req_json(url: str):
    """Make a request with Clove user-agent header and return json response"""
    resp = clove_req(url)
    if not resp or resp.status != 200:
        return

    return json.loads(resp.read().decode())


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
    logger.debug(
        'Found transaction from %s with fees %.8f',
        datetime.fromtimestamp(tx_details['timestamp']).isoformat(),
        tx_details['fees'],
    )
    return tx_details['fees']


def get_fee_from_last_transactions(network: str, tx_limit: int=5) -> Optional[float]:
    """Counting fee based on tx_limit transactions (max 10)"""

    last_transactions = get_last_transactions(network)[:tx_limit]

    fees = []

    for tx_hash in last_transactions:

        tx_size = get_transaction_size(network, tx_hash)
        if not tx_size:
            continue

        tx_fee = get_transaction_fee(network, tx_hash)
        if not tx_fee:
            continue

        tx_fee_per_kb = (tx_fee * 1000) / tx_size
        fees.append(tx_fee_per_kb)

    return round(sum(fees) / len(fees), 8) if fees else None


def get_fee_from_blockcypher(network: str, testnet: bool=False) -> Optional[float]:
    """Returns current high priority (1-2 blocks) fee estimates."""
    subnet = 'test3' if testnet else 'main'
    resp = clove_req(f'https://api.blockcypher.com/v1/{network}/{subnet}')
    if resp.status != 200:
        logger.debug('Unexpected status code from blockcypher: %d', resp.status)
        return
    data = json.loads(resp.read().decode())
    return data['high_fee_per_kb'] / COIN


cryptoid_api_key = os.getenv('CRYPTOID_API_KEY')


def get_utxo(
    network: str, address: str, amount: float, use_blockcypher: bool=False, testnet: bool=False
) -> Optional[list]:
    if use_blockcypher:
        subnet = 'test3' if testnet else 'main'
        api_url = f'https://api.blockcypher.com/v1/{network}/{subnet}/addrs/{address}' \
                  f'?limit=2000&unspentOnly=true&includeScript=true&confirmations=6'
        unspent_key = 'txrefs'
        vout_key = 'tx_output_n'
    else:
        api_url = f'https://chainz.cryptoid.info/{network}/api.dws?q=unspent&key={cryptoid_api_key}&active={address}'
        unspent_key = 'unspent_outputs'
        vout_key = 'tx_ouput_n'

    utxo = []
    total = 0

    data = clove_req_json(api_url)
    if data is None:
        logger.debug('Could not get UTXOs for address %s in %s network', address, network)
        return

    unspent = data.get(unspent_key, [])

    if not use_blockcypher:
        for output in unspent:
            output['value'] = int(output['value'])

    unspent = sorted(unspent, key=lambda k: k['value'], reverse=True)
    for output in unspent:
        value = satoshi_to_btc(output['value'])
        utxo.append(
            Utxo(
                tx_id=output['tx_hash'],
                vout=output[vout_key],
                value=value,
                tx_script=output['script'],
            )
        )
        total += value
        if total > amount:
            return utxo

    logger.debug(f'Cannot find enough UTXO\'s. Found {total:.8f} from {amount:.8f}.')
