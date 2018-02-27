import logging

import coloredlogs

from clove.constants import COLORED_LOGS_STYLES

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
coloredlogs.install(logger=logger, level=logging.DEBUG, level_styles=COLORED_LOGS_STYLES)
