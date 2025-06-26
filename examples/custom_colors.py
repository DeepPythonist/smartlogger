#!/usr/bin/env python3

import logging
import smartlogger
from smartlogger.config.colors import ANSIColors

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

print("=== Default Colors ===")
logger.debug("Default debug (blue)")
logger.info("Default info (green)")
logger.warning("Default warning (yellow)")
logger.error("Default error (red)")
logger.critical("Default critical (bold red)")

print("\n=== Custom Colors ===")
smartlogger.configure_colors({
    'DEBUG': ANSIColors.CYAN,
    'INFO': ANSIColors.BRIGHT_GREEN,
    'WARNING': ANSIColors.MAGENTA,
    'ERROR': ANSIColors.BRIGHT_RED,
    'CRITICAL': ANSIColors.BOLD + ANSIColors.YELLOW + ANSIColors.BG_RED
})

logger.debug("Custom debug (cyan)")
logger.info("Custom info (bright green)")
logger.warning("Custom warning (magenta)")
logger.error("Custom error (bright red)")
logger.critical("Custom critical (bold yellow on red background)")

print("\nCustom color configuration completed!") 