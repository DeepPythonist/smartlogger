import os
import sys
import platform
from typing import Optional, Dict, Any

from ..exceptions import TerminalDetectionError


class TerminalCapabilities:
    def __init__(self):
        self._capabilities = self._detect_capabilities()
    
    def _detect_capabilities(self) -> Dict[str, Any]:
        capabilities = {
            'colors': self._supports_colors(),
            'ansi': self._supports_ansi(),
            'interactive': self._is_interactive(),
            'platform': self._get_platform_info(),
            'term_program': self._get_term_program(),
            'color_depth': self._get_color_depth()
        }
        return capabilities
    
    def _supports_colors(self) -> bool:
        try:
            if os.environ.get('NO_COLOR'):
                return False
            
            if os.environ.get('FORCE_COLOR'):
                return True
            
            if not self._is_interactive():
                return False
            
            if platform.system() == 'Windows':
                return self._windows_supports_ansi()
            
            term = os.environ.get('TERM', '').lower()
            if term in ('dumb', 'unknown', ''):
                return False
            
            return True
        except Exception:
            return False
    
    def _supports_ansi(self) -> bool:
        try:
            if platform.system() == 'Windows':
                return self._windows_supports_ansi()
            return True
        except Exception:
            return False
    
    def _is_interactive(self) -> bool:
        try:
            return (
                hasattr(sys.stdout, 'isatty') and 
                sys.stdout.isatty() and
                hasattr(sys.stderr, 'isatty') and 
                sys.stderr.isatty()
            )
        except Exception:
            return False
    
    def _get_platform_info(self) -> Dict[str, str]:
        return {
            'system': platform.system(),
            'release': platform.release(),
            'version': platform.version(),
            'machine': platform.machine()
        }
    
    def _get_term_program(self) -> Optional[str]:
        return os.environ.get('TERM_PROGRAM')
    
    def _get_color_depth(self) -> int:
        colorterm = os.environ.get('COLORTERM', '').lower()
        if colorterm in ('truecolor', '24bit'):
            return 24
        elif colorterm in ('256color', '256'):
            return 8
        
        term = os.environ.get('TERM', '').lower()
        if '256color' in term or '256' in term:
            return 8
        elif 'color' in term:
            return 4
        
        return 1
    
    def _windows_supports_ansi(self) -> bool:
        if platform.system() != 'Windows':
            return True
        
        try:
            version = platform.version()
            major, minor, build = map(int, version.split('.'))
            return (major, minor, build) >= (10, 0, 14393)
        except Exception:
            return False
    
    def supports_colors(self) -> bool:
        return self._capabilities.get('colors', False)
    
    def supports_ansi(self) -> bool:
        return self._capabilities.get('ansi', False)
    
    def is_interactive(self) -> bool:
        return self._capabilities.get('interactive', False)
    
    def get_color_depth(self) -> int:
        return self._capabilities.get('color_depth', 1)
    
    def get_platform_info(self) -> Dict[str, str]:
        return self._capabilities.get('platform', {})
    
    def get_term_program(self) -> Optional[str]:
        return self._capabilities.get('term_program')


_terminal_capabilities = None


def get_terminal_capabilities() -> TerminalCapabilities:
    global _terminal_capabilities
    if _terminal_capabilities is None:
        _terminal_capabilities = TerminalCapabilities()
    return _terminal_capabilities


def supports_colors() -> bool:
    try:
        return get_terminal_capabilities().supports_colors()
    except Exception:
        return False


def supports_ansi() -> bool:
    try:
        return get_terminal_capabilities().supports_ansi()
    except Exception:
        return False


def is_interactive_terminal() -> bool:
    try:
        return get_terminal_capabilities().is_interactive()
    except Exception:
        return False


def get_color_depth() -> int:
    try:
        return get_terminal_capabilities().get_color_depth()
    except Exception:
        return 1 