#!/usr/bin/env python3

import logging
import sys
from smartlogger import (
    ColoredStreamHandler, 
    ColoredFormatter,
    MinimalColoredFormatter,
    DetailedColoredFormatter
)

print("=== Manual Integration Example ===")

# Create logger
logger = logging.getLogger('integration_demo')
logger.setLevel(logging.DEBUG)

# Remove default handlers
logger.handlers.clear()

# Add colored console handler
console_handler = ColoredStreamHandler(sys.stdout)
console_handler.setFormatter(MinimalColoredFormatter())
logger.addHandler(console_handler)

print("\n1. Minimal formatter:")
logger.info("Simple info message")
logger.error("Simple error message")

# Change to detailed formatter
console_handler.setFormatter(DetailedColoredFormatter())

print("\n2. Detailed formatter:")
logger.info("Detailed info message")
logger.error("Detailed error message")

# Add file handler (without colors)
file_handler = logging.FileHandler('app.log')
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
))
logger.addHandler(file_handler)

print("\n3. Dual output (console + file):")
logger.info("This goes to both console (colored) and file (plain)")
logger.warning("Warning message in both outputs")

# Clean up
logger.handlers.clear()

print("\nIntegration example completed!")
print("Check 'app.log' file for plain text logs.") 