from colorama import Fore, Style


def log_inappropriate_response_messages(logger, messages, node):
    messages_length = len(messages)
    messages = ', '.join([message.command.decode('ascii') for message in messages])
    if messages_length == 0:
        log_debug(logger, f"[{node}] Couldn't retrieve any deserializable message.")
    elif messages_length == 1:
        log_debug(logger, f"[{node}] Node response message was: '{messages}', whilst it should be 'getdata'.")
    else:
        log_debug(logger, f"[{node}] Node response messages were: '{messages}', whilst it should be 'getdata'.")


def log_info(logger, logging_message: str):
    logger.info(f'{Fore.GREEN}{logging_message}{Style.RESET_ALL}')


def log_debug(logger, logging_message: str):
    logger.debug(f'{Fore.MAGENTA}{logging_message}{Style.RESET_ALL}')


def log_exception(logger, exception: Exception):
    exception.message = f'{Fore.RED}{exception.message}{Style.RESET_ALL}'
    logger.exception(exception.message)
