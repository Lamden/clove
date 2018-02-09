from colorama import Fore, Style


def log_inappropriate_response_messages(logger, messages):
    messages_length = len(messages)
    messages = ', '.join([message.command.decode('ascii') for message in messages])
    if messages_length == 0:
        logger.debug(purplify("Couldn't retrieve any deserializable message."))
    elif messages_length == 1:
        logger.debug(purplify(f"Node response message was: '{messages}', whilst it should be 'getdata'."))
    else:
        logger.debug(purplify(f"Node response messages were: '{messages}', whilst it should be 'getdata'."))
    Style.RESET_ALL


def greenify(logging_message: str):
    return f'{Fore.GREEN}{logging_message}{Style.RESET_ALL}'


def purplify(logging_message: str):
    return f'{Fore.MAGENTA}{logging_message}{Style.RESET_ALL}'


def redify(logging_message: str):
    return f'{Fore.RED}{logging_message}{Style.RESET_ALL}'
