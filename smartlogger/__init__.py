__version__ = "0.1.0"
__author__ = "SmartLogger Team"
__description__ = "Colorful logging extension for Python logging module"

from .config.colors import (
    ColorScheme,
    configure_colors,
    enable_colors,
    disable_colors,
    get_default_scheme
)

from .core.handler import (
    ColoredStreamHandler,
    ColoredConsoleHandler,
    ColoredFileHandler,
    SmartColorHandler,
    DualOutputHandler
)

from .core.formatter import (
    ColoredFormatter,
    MinimalColoredFormatter,
    DetailedColoredFormatter,
    JSONColoredFormatter
)

from .core.monkey_patch import (
    patch_logging,
    unpatch_logging,
    patch_logger,
    is_patched,
    get_patched_loggers
)

from .exceptions import (
    SmartLoggerError,
    ConfigurationError,
    ColorFormatError,
    TerminalDetectionError,
    HandlerCreationError,
    FormatterError,
    PatchingError,
    UnsupportedPlatformError
)

from .utils.terminal import (
    supports_colors,
    supports_ansi,
    is_interactive_terminal,
    get_color_depth,
    get_terminal_capabilities
)

from .utils.compatibility import (
    get_python_version,
    is_python_version_supported,
    check_compatibility
)


__all__ = [
    '__version__',
    '__author__',
    '__description__',
    
    'ColorScheme',
    'configure_colors',
    'enable_colors',
    'disable_colors',
    'get_default_scheme',
    
    'ColoredStreamHandler',
    'ColoredConsoleHandler',
    'ColoredFileHandler',
    'SmartColorHandler',
    'DualOutputHandler',
    
    'ColoredFormatter',
    'MinimalColoredFormatter',
    'DetailedColoredFormatter',
    'JSONColoredFormatter',
    
    'patch_logging',
    'unpatch_logging',
    'patch_logger',
    'is_patched',
    'get_patched_loggers',
    
    'SmartLoggerError',
    'ConfigurationError',
    'ColorFormatError',
    'TerminalDetectionError',
    'HandlerCreationError',
    'FormatterError',
    'PatchingError',
    'UnsupportedPlatformError',
    
    'supports_colors',
    'supports_ansi',
    'is_interactive_terminal',
    'get_color_depth',
    'get_terminal_capabilities',
    
    'get_python_version',
    'is_python_version_supported',
    'check_compatibility',
]


def get_version() -> str:
    return __version__


def get_info() -> dict:
    return {
        'version': __version__,
        'author': __author__,
        'description': __description__,
        'python_version': get_python_version(),
        'supports_colors': supports_colors(),
        'terminal_capabilities': get_terminal_capabilities().__dict__,
        'is_patched': is_patched()
    } 