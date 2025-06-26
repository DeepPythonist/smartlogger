#!/usr/bin/env python3

# تست رنگ ANSI مستقیم
print("تست رنگ‌های ANSI:")
print("\033[31mقرمز\033[0m")
print("\033[32mسبز\033[0m") 
print("\033[33mزرد\033[0m")
print("\033[34mآبی\033[0m")

# تست با SmartLogger
print("\nتست SmartLogger:")

import logging
import sys
import os

# فعال کردن force color
os.environ['FORCE_COLOR'] = '1'

# Import SmartLogger
import smartlogger
from smartlogger import ColoredStreamHandler, ColoredFormatter

# ایجاد handler مخصوص
handler = ColoredStreamHandler(sys.stdout, force_color=True)
formatter = ColoredFormatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)

# ایجاد logger
logger = logging.getLogger('test')
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

print("لاگ‌های رنگی:")
logger.debug("DEBUG message")
logger.info("INFO message")
logger.warning("WARNING message") 
logger.error("ERROR message")
logger.critical("CRITICAL message") 