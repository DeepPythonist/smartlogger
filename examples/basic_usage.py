#!/usr/bin/env python3

import logging
import smartlogger.auto

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("This is a debug message - should appear in blue")
logger.info("This is an info message - should appear in green") 
logger.warning("This is a warning message - should appear in yellow")
logger.error("This is an error message - should appear in red")
logger.critical("This is a critical message - should appear in bold red")

print("\nBasic SmartLogger usage completed!")
print("Notice how the log levels are colorized automatically.") 