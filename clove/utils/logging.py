import logging

import coloredlogs

from clove.constants import COLORED_LOGS_STYLES

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
coloredlogs.install(logger=logger, level=logging.DEBUG, level_styles=COLORED_LOGS_STYLES)


def log_inappropriate_response_messages(logger, messages, node):
    messages_length = len(messages)
    messages = ', '.join([message.command.decode('ascii') for message in messages])
    if messages_length == 0:
        logger.debug(f"[{node}] Couldn't retrieve any deserializable message.")
    elif messages_length == 1:
        logger.debug(f"[{node}] Node response message was: '{messages}', whilst it should be 'getdata'.")
    else:
        logger.debug(f"[{node}] Node response messages were: '{messages}', whilst it should be 'getdata'.")
