class CloveException(Exception):

    def __init__(self, message=None, node=None):
        self.message = f'[{node}] {message}' if node else message


class ConnectionProblem(CloveException):
    pass


class TransactionRejected(CloveException):
    pass


class UnexpectedResponseFromNode(CloveException):
    pass


class ImpossibleDeserialization(CloveException):
    pass


class UnsupportedTransactionType(CloveException):
    pass
