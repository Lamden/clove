from http.client import HTTPResponse
import json
import os
import time
from typing import Optional
from urllib.error import HTTPError, URLError
import urllib.request

from clove.constants import (
    BLOCKCYPHER_SUPPORTED_NETWORKS,
    CLOVE_API_URL,
    CRYPTOID_SUPPORTED_NETWORKS,
    NETWORKS_WITH_API,
)
from clove.utils.bitcoin import from_base_units
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


def get_transaction(network: str, tx_hash: str, testnet: bool=False) -> Optional[dict]:

    symbol = network.lower()
    if symbol not in NETWORKS_WITH_API and symbol != 'RVN':
        raise ValueError('This network has no API.')

    if symbol in BLOCKCYPHER_SUPPORTED_NETWORKS:
        if testnet and symbol != 'btc':
            raise ValueError('Only BTC testnet is supported')
        network_url = 'test3' if testnet else 'main'
        api_url = f'https://api.blockcypher.com/v1/{symbol}/{network_url}/txs/{tx_hash}?limit=50&includeHex=true'
        return clove_req_json(api_url)

    if symbol == 'RVN':
        return clove_req_json(f'http://raven-blockchain.info/api/getrawtransaction?txid={tx_hash}&decrypt=1')

    return clove_req_json(f'https://chainz.cryptoid.info/{symbol}/api.dws?q=txinfo&t={tx_hash}')


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


def get_current_fee(network: str) -> Optional[float]:
    """Getting current network fee from Clove API"""

    resp = clove_req_json(f'{CLOVE_API_URL}/fee/{network}')

    if not resp:
        logger.debug('Could not get current fee for %s network', network)
        return

    return resp['fee']


def get_balance(network: object, address: str):

    network_symbol = network.default_symbol.lower()
    if network_symbol not in NETWORKS_WITH_API:
        logger.debug('Unsupported network %s', network.default_symbol)
        return

    if network_symbol in BLOCKCYPHER_SUPPORTED_NETWORKS:
        return get_balance_blockcypher(network.default_symbol, address, network.is_test_network())

    if network_symbol in CRYPTOID_SUPPORTED_NETWORKS:
        return get_balance_cryptoid(
            network.default_symbol,
            address,
            network.is_test_network(),
            os.getenv('CRYPTOID_API_KEY'),
        )


def get_balance_blockcypher(network: str, address: str, testnet: bool) -> Optional[float]:
    subnet = 'test3' if testnet else 'main'
    url = f'https://api.blockcypher.com/v1/{network.lower()}/{subnet}/addrs/{address}/full?limit=2000'
    data = clove_req_json(url)
    if data is None:
        logger.debug('Could not get details for address %s in %s network', address, network)
        return
    return from_base_units(data['balance'])


def get_balance_cryptoid(network: str, address: str, testnet: bool, cryptoid_api_key: str) -> Optional[float]:
    if cryptoid_api_key is None:
        raise ValueError('API key for cryptoid is required to get balance.')
    network = network.lower()
    if testnet:
        network += '-TEST'
    url = f'https://chainz.cryptoid.info/{network}/api.dws?q=getbalance&a={address}&key={cryptoid_api_key}'
    data = clove_req_json(url)
    if data is None:
        logger.debug('Could not get details for address %s in %s network', address, network)
        return
    return data


def get_utxo_from_api(
    network: str,
    address: str,
    amount: float,
    use_blockcypher: bool=False,
    testnet: bool=False,
    cryptoid_api_key: str=None
) -> Optional[list]:
    from clove.network.bitcoin.utxo import Utxo

    if use_blockcypher:
        subnet = 'test3' if testnet else 'main'
        api_url = f'https://api.blockcypher.com/v1/{network}/{subnet}/addrs/{address}' \
                  f'?limit=2000&unspentOnly=true&includeScript=true&confirmations=6'
        unspent_key = 'txrefs'
        vout_key = 'tx_output_n'
    elif cryptoid_api_key is None:
        raise ValueError('API key for cryptoid is required to get UTXOs.')
    else:
        api_url = f'https://chainz.cryptoid.info/{network}/api.dws?q=unspent&key={cryptoid_api_key}&active={address}'
        unspent_key = 'unspent_outputs'
        vout_key = 'tx_ouput_n'

    data = clove_req_json(api_url)
    if data is None:
        logger.debug('Could not get UTXOs for address %s in %s network', address, network)
        return

    unspent = data.get(unspent_key, [])

    for output in unspent:
        output['value'] = int(output['value'])

    unspent = sorted(unspent, key=lambda k: k['value'], reverse=True)

    utxo = []
    total = 0

    for output in unspent:
        value = from_base_units(output['value'])
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

    logger.debug(f'Cannot find enough UTXO\'s. Found %.8f from %.8f.', total, amount)


def extract_scriptsig_from_redeem_transaction(
    network: str,
    contract_address: str,
    testnet: bool=False,
    cryptoid_api_key: str=None,
) -> Optional[str]:

    network = network.lower()

    if network != 'btc' and testnet:
        raise NotImplementedError

    if network in ('btc', 'doge', 'dash'):
        return extract_scriptsig_blockcypher(network, contract_address, testnet)

    if network == 'rvn':
        return extract_scriptsig_raven(contract_address, testnet)

    if network not in CRYPTOID_SUPPORTED_NETWORKS:
        raise NotImplementedError

    return extract_scriptsig_cryptoid(network, contract_address, testnet, cryptoid_api_key)


def extract_scriptsig_blockcypher(network: str, contract_address: str, testnet: bool=False) -> Optional[str]:
    subnet = 'test3' if testnet else 'main'
    data = clove_req_json(f'https://api.blockcypher.com/v1/{network}/{subnet}/addrs/{contract_address}/full')
    if not data:
        logger.debug('Unexpected response from blockcypher')
        raise ValueError('Unexpected response from blockcypher')

    transactions = data['txs']
    if len(transactions) == 1:
        logger.debug('Contract was not redeemed yet.')
        return

    return transactions[0]['inputs'][0]['script']


def extract_scriptsig_cryptoid(
    network: str,
    contract_address: str,
    testnet: bool=False,
    cryptoid_api_key: str=None,
) -> Optional[str]:

    if not cryptoid_api_key:
        raise ValueError('API key for cryptoid is required.')

    url = f'https://chainz.cryptoid.info/ltc/api.dws?q=multiaddr&active={contract_address}&key={cryptoid_api_key}'
    data = clove_req_json(url)
    if not data:
        logger.debug('Unexpected response from cryptoid')
        raise ValueError('Unexpected response from cryptoid')

    transactions = data['txs']
    if len(transactions) == 1:
        logger.debug('Contract was not redeemed yet.')
        return

    redeem_tx_hash = transactions[0]['hash']
    url = f'https://chainz.cryptoid.info/explorer/tx.raw.dws?coin={network}&id={redeem_tx_hash}'
    data = clove_req_json(url)
    if not data:
        logger.debug('Unexpected response from cryptoid')
        raise ValueError('Unexpected response from cryptoid')

    return data['vin'][0]['scriptSig']['hex']


def extract_scriptsig_raven(contract_address: str, testnet: bool=False) -> Optional[str]:

    data = clove_req_json(f'http://raven-blockchain.info/ext/getaddress/{contract_address}')
    if not data:
        logger.debug('Unexpected response from Ravencoin API.')
        raise ValueError('Unexpected response from Ravencoin API.')

    transactions = data['last_txs']
    if len(transactions) == 1:
        logger.debug('Contract was not redeemed yet.')
        return

    redeem_tx_hash = transactions[0]['addresses']
    data = clove_req_json(f'http://raven-blockchain.info/api/getrawtransaction?txid={redeem_tx_hash}&decrypt=1')
    if not data:
        logger.debug('Unexpected response from Ravencoin API.')
        raise ValueError('Unexpected response from Ravencoin API.')

    return data['vin'][0]['scriptSig']['hex']


def find_redeem_transaction(
    recipient_address: str,
    contract_address: str,
    value: int,
    subdomain: str,
) -> Optional[str]:

    recipient_address = recipient_address.lower()
    contract_address = contract_address.lower()
    value = str(value)

    etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')
    if not etherscan_api_key:
        raise ValueError('API key for etherscan is required.')

    data = clove_req_json(
        f'http://{subdomain}.etherscan.io/api?module=account&action=txlistinternal'
        f'&address={recipient_address}&apikey={etherscan_api_key}'
    )

    for result in reversed(data['result']):
        if result['to'] == recipient_address and result['from'] == contract_address and result['value'] == value:
            return result['hash']

    logger.debug('Redeem transaction not found.')


def find_redeem_token_transaction(
    recipient_address: str,
    token_address: str,
    value: int,
    subdomain: str
) -> Optional[str]:

    recipient_address = recipient_address.lower()
    token_address = token_address.lower()
    value = str(value)

    etherscan_api_key = os.getenv('ETHERSCAN_API_KEY')
    if not etherscan_api_key:
        raise ValueError('API key for etherscan is required.')

    data = clove_req_json(
        f'http://{subdomain}.etherscan.io/api?module=account&action=tokentx'
        f'&contractaddress={token_address}&address={recipient_address}'
        f'&apikey={etherscan_api_key}'
    )

    for result in reversed(data['result']):
        if result['to'] == recipient_address \
                and result['contractAddress'] == token_address \
                and result['value'] == value:
            return result['hash']

    logger.debug('Redeem token transaction not found.')
