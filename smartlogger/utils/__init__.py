# Utilities package 

from .terminal import (
    TerminalCapabilities,
    get_terminal_capabilities,
    supports_colors,
    supports_ansi,
    is_interactive_terminal,
    get_color_depth
)

from .compatibility import (
    get_python_version,
    is_python_version_supported,
    check_compatibility,
    safe_getattr,
    safe_hasattr,
    safe_isinstance,
    safe_callable,
    CompatibilityError
)

__all__ = [
    'TerminalCapabilities',
    'get_terminal_capabilities',
    'supports_colors',
    'supports_ansi',
    'is_interactive_terminal',
    'get_color_depth',
    'get_python_version',
    'is_python_version_supported',
    'check_compatibility',
    'safe_getattr',
    'safe_hasattr',
    'safe_isinstance',
    'safe_callable',
    'CompatibilityError'
] 