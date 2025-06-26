import logging
from smartlogger.core.formatter import ColorFormatter
from smartlogger.core.handler import ColorHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = ColorHandler()
formatter = ColorFormatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

logger.debug("Custom formatted debug message")
logger.info("Custom formatted info message")
logger.warning("Custom formatted warning message")
logger.error("Custom formatted error message")
logger.critical("Custom formatted critical message") 