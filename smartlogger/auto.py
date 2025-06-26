import sys
import logging
from .core.monkey_patch import patch_logging

try:
    patch_logging()
except Exception:
    pass 