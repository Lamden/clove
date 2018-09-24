class BaseAPI(object):

    API = True

    @classmethod
    def get_confirmations_from_tx_json(cls, tx_json: dict) -> int:
        return tx_json['confirmations']
