from typing import Optional
import os

from clove.utils.external_source import clove_req_json
from clove.utils.logging import logger


class cmcAPI(object):
    '''Adapter class for blockcypher.com'''

    cmc_api_url = 'https://pro-api.coinmarketcap.com'
    '''Base url for coin market cap API.'''

    @classmethod
    def cmc_url(cls) -> str:
        '''
        This method returns a full API url for a given network.

        Returns:
            str: full API url
        '''
        return f'{cls.cmc_api_url}/v1/'
    
    @classmethod
    def cmc_headers(cls) -> dict:
        api_key = os.environ.get('CMC_API_KEY')
        if not api_key:
            raise ValueError('CMC_API_KEY environment variable was not set.')

        return {'User-Agent': 'Clove',
                'Content-Type' : 'application/json',
                'X-CMC_PRO_API_KEY': api_key}

    @classmethod
    def get_info(cls, symbol: str) -> Optional[dict]:
        '''
        Returns the cmc info for a coin.

        Returns:
            coin details info

        Example:
            >>> from clove.network import Bitcoin
            >>> network = Bitcoin()
            >>> network.cmc_api.cmc_info()
            https://sandbox.coinmarketcap.com/api/v1/#operation/getV1CryptocurrencyInfo
        '''
        url = f'{cls.cmc_url()}cryptocurrency/info?symbol={symbol}'
        print(url)
        return clove_req_json(f'{cls.cmc_url()}cryptocurrency/info?symbol={symbol}', cls.cmc_headers())

    @classmethod
    def get_prices(cls, symbols: list, currency: str) -> Optional[dict]:
        '''
        Returns the cmc price info for a coin.

        Returns:
            coin price info

        Example:
            >>> from clove.network import Bitcoin
            >>> network = Bitcoin()
            >>> network.cmc_api.cmc_prices()
            https://sandbox.coinmarketcap.com/api/v1/#operation/getV1CryptocurrencyQuotesLatest
        '''
        symbolsStr = ",".join(symbols)
        return clove_req_json(f'{cls.cmc_url()}cryptocurrency/quotes/latest?symbol={symbolsStr}&convert={currency}', cls.cmc_headers())