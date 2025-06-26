# Auto-discovery and activation module 

import sys
import logging
import atexit
from typing import Optional

from .core.monkey_patch import patch_logging, unpatch_logging, is_patched
from .config.colors import get_default_scheme, configure_colors
from .utils.compatibility import check_compatibility
from .utils.terminal import supports_colors
from .exceptions import SmartLoggerError


class AutoConfigurator:
    _instance = None
    _activated = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._original_logging_imported = 'logging' in sys.modules
            self.activate()
    
    def activate(self) -> bool:
        if self._activated:
            return True
        
        try:
            check_compatibility()
            
            if not supports_colors():
                return False
            
            success = patch_logging(
                patch_root=True,
                preserve_existing=True,
                add_colored_handler=True
            )
            
            if success:
                self._activated = True
                atexit.register(self.deactivate)
                return True
            
            return False
            
        except Exception:
            return False
    
    def deactivate(self) -> bool:
        if not self._activated:
            return True
        
        try:
            success = unpatch_logging()
            if success:
                self._activated = False
            return success
        except Exception:
            return False
    
    def is_active(self) -> bool:
        return self._activated and is_patched()
    
    def configure_colors(self, colors: dict) -> bool:
        try:
            configure_colors(colors)
            return True
        except Exception:
            return False


_auto_configurator = None


def _ensure_configurator():
    global _auto_configurator
    if _auto_configurator is None:
        _auto_configurator = AutoConfigurator()
    return _auto_configurator


def activate() -> bool:
    return _ensure_configurator().activate()


def deactivate() -> bool:
    return _ensure_configurator().deactivate()


def is_active() -> bool:
    return _ensure_configurator().is_active()


def configure_colors(colors: dict) -> bool:
    return _ensure_configurator().configure_colors(colors)


try:
    _ensure_configurator()
except Exception:
    pass 