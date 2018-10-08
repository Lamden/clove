import logging

import coloredlogs

from clove.constants import COLORED_LOGS_STYLES

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
'''Common logger for all the clove methods.'''
coloredlogs.install(logger=logger, level=logging.DEBUG, level_styles=COLORED_LOGS_STYLES)
