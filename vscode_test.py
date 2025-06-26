#!/usr/bin/env python3
"""
تست خاص برای VSCode Terminal
"""

import os
import sys

# فعال کردن رنگ‌ها در VSCode
os.environ['FORCE_COLOR'] = '1'
os.environ['COLORTERM'] = 'truecolor'

print("🎨 VSCode Color Test")
print("=" * 30)

# تست ANSI مستقیم با force
print("مستقیم ANSI:")
print(f"\033[91mقرمز روشن\033[0m")  # Bright red
print(f"\033[92mسبز روشن\033[0m")   # Bright green  
print(f"\033[93mزرد روشن\033[0m")   # Bright yellow
print(f"\033[94mآبی روشن\033[0m")   # Bright blue

# تست با SmartLogger
print("\nSmartLogger:")
import logging

# Force import
import smartlogger
from smartlogger.config.colors import ANSIColors

# تنظیم رنگ‌های روشن‌تر
smartlogger.configure_colors({
    'DEBUG': ANSIColors.BRIGHT_BLUE,
    'INFO': ANSIColors.BRIGHT_GREEN,
    'WARNING': ANSIColors.BRIGHT_YELLOW,
    'ERROR': ANSIColors.BRIGHT_RED,
    'CRITICAL': ANSIColors.BOLD + ANSIColors.BRIGHT_RED
})

# ایجاد logger با force color
from smartlogger import ColoredStreamHandler, ColoredFormatter

handler = ColoredStreamHandler(sys.stdout, force_color=True)
formatter = ColoredFormatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger('VSCodeTest')
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.debug("DEBUG - آبی روشن")
logger.info("INFO - سبز روشن") 
logger.warning("WARNING - زرد روشن")
logger.error("ERROR - قرمز روشن")
logger.critical("CRITICAL - قرمز Bold")

print("\n✅ اگر رنگ‌ها را می‌بینید، SmartLogger کار می‌کند!")
print("🔧 اگر رنگ‌ها را نمی‌بینید:")
print("   1. در Terminal.app اجرا کنید")
print("   2. VSCode settings را بررسی کنید")
print("   3. از iTerm2 استفاده کنید") 