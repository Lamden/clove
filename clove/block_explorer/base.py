class BaseAPI(object):
    '''Common class for all the block explorers adapter classes.'''

    API = True
    '''This value tells us that a given network have a block explorer API support.'''

    @classmethod
    def get_confirmations_from_tx_json(cls, tx_json: dict) -> int:
        '''
        This is an adapter method for getting the number of confirmatons from transaction details.

        This method may be halpfull in a future if some block explorers
        will store the number of confirmations under the different key name.
        '''
        return tx_json['confirmations']
