# Color definitions and configurations 

import os
import sys
from typing import Dict, Optional


class ANSIColors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Regular colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    # Bright colors
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    # Background colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'
    BG_MAGENTA = '\033[45m'
    BG_CYAN = '\033[46m'
    BG_WHITE = '\033[47m'


class ColorScheme:
    def __init__(self, colors: Optional[Dict[str, str]] = None):
        self._colors = colors or self._get_default_colors()
        self._enabled = self._should_enable_colors()
    
    def _get_default_colors(self) -> Dict[str, str]:
        return {
            'DEBUG': ANSIColors.BRIGHT_BLUE,
            'INFO': ANSIColors.GREEN,
            'WARNING': ANSIColors.YELLOW,
            'ERROR': ANSIColors.RED,
            'CRITICAL': ANSIColors.BOLD + ANSIColors.RED + ANSIColors.BG_WHITE
        }
    
    def _should_enable_colors(self) -> bool:
        if os.environ.get('NO_COLOR'):
            return False
        
        if os.environ.get('FORCE_COLOR'):
            return True
        
        if not hasattr(sys.stdout, 'isatty'):
            return False
        
        if not sys.stdout.isatty():
            return False
        
        term = os.environ.get('TERM', '').lower()
        if term in ('dumb', 'unknown'):
            return False
        
        return True
    
    def get_color(self, level: str) -> str:
        if not self._enabled:
            return ''
        return self._colors.get(level.upper(), '')
    
    def get_reset(self) -> str:
        if not self._enabled:
            return ''
        return ANSIColors.RESET
    
    def update_colors(self, colors: Dict[str, str]) -> None:
        self._colors.update(colors)
    
    def enable(self) -> None:
        self._enabled = True
    
    def disable(self) -> None:
        self._enabled = False
    
    @property
    def enabled(self) -> bool:
        return self._enabled


_default_scheme = ColorScheme()


def get_default_scheme() -> ColorScheme:
    return _default_scheme


def configure_colors(colors: Dict[str, str]) -> None:
    _default_scheme.update_colors(colors)


def enable_colors() -> None:
    _default_scheme.enable()


def disable_colors() -> None:
    _default_scheme.disable() 