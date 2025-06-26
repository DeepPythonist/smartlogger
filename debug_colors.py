#!/usr/bin/env python3
"""
تشخیص مشکل رنگ‌ها در SmartLogger
"""

import os
import sys
import logging

print("🔍 SmartLogger Color Debugging")
print("=" * 40)

# بررسی محیط
print("📋 Environment Check:")
print(f"  Python version: {sys.version}")
print(f"  Platform: {sys.platform}")
print(f"  stdout.isatty(): {sys.stdout.isatty()}")
print(f"  stderr.isatty(): {sys.stderr.isatty()}")
print(f"  NO_COLOR env: {os.environ.get('NO_COLOR', 'Not set')}")
print(f"  FORCE_COLOR env: {os.environ.get('FORCE_COLOR', 'Not set')}")
print(f"  TERM env: {os.environ.get('TERM', 'Not set')}")

# تست ANSI مستقیم
print("\n🎨 Direct ANSI Test:")
print(f"  Red: \033[31mThis should be RED\033[0m")
print(f"  Green: \033[32mThis should be GREEN\033[0m")
print(f"  Yellow: \033[33mThis should be YELLOW\033[0m")
print(f"  Blue: \033[34mThis should be BLUE\033[0m")

# تست SmartLogger قبل از import
print("\n🧪 SmartLogger Test:")

try:
    # Import SmartLogger
    print("  Importing smartlogger.auto...")
    import smartlogger.auto
    print("  ✅ Import successful")
    
    # بررسی وضعیت activation
    from smartlogger.auto import is_active
    print(f"  SmartLogger active: {is_active()}")
    
    # بررسی قابلیت‌های ترمینال
    from smartlogger.utils.terminal import supports_colors, get_terminal_capabilities
    print(f"  Terminal supports colors: {supports_colors()}")
    
    caps = get_terminal_capabilities()
    print(f"  Terminal capabilities: {caps.__dict__}")
    
except Exception as e:
    print(f"  ❌ Import failed: {e}")
    sys.exit(1)

# تست logging با force color
print("\n🎯 Forced Color Test:")
from smartlogger import ColoredStreamHandler, ColoredFormatter

# ایجاد handler با force color
handler = ColoredStreamHandler(sys.stdout, force_color=True)
formatter = ColoredFormatter('%(levelname)s: %(message)s')
handler.setFormatter(formatter)

logger = logging.getLogger('ForceColorTest')
logger.handlers.clear()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

print("  Testing with force_color=True:")
logger.debug("DEBUG - This should be BLUE")
logger.info("INFO - This should be GREEN")  
logger.warning("WARNING - This should be YELLOW")
logger.error("ERROR - This should be RED")
logger.critical("CRITICAL - This should be BOLD RED")

# تست بدون force color
print("\n🔧 Normal Color Test:")
normal_handler = ColoredStreamHandler(sys.stdout)
normal_formatter = ColoredFormatter('%(levelname)s: %(message)s')
normal_handler.setFormatter(normal_formatter)

normal_logger = logging.getLogger('NormalColorTest')
normal_logger.handlers.clear()
normal_logger.addHandler(normal_handler)
normal_logger.setLevel(logging.DEBUG)

print("  Testing with auto-detection:")
normal_logger.debug("DEBUG - Auto color")
normal_logger.info("INFO - Auto color")
normal_logger.warning("WARNING - Auto color")
normal_logger.error("ERROR - Auto color")
normal_logger.critical("CRITICAL - Auto color")

print("\n📊 Summary:")
print("  If you see colors above, SmartLogger is working!")
print("  If not, your terminal may not support ANSI colors.")
print("  Try running with: FORCE_COLOR=1 python debug_colors.py") 