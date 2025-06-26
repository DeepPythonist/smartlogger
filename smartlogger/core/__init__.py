# Core functionality package 

from .handler import (
    ColoredStreamHandler,
    ColoredConsoleHandler,
    ColoredFileHandler,
    SmartColorHandler,
    DualOutputHandler
)

from .formatter import (
    ColoredFormatter,
    MinimalColoredFormatter,
    DetailedColoredFormatter,
    JSONColoredFormatter
)

from .monkey_patch import (
    LoggingPatcher,
    patch_logging,
    unpatch_logging,
    patch_logger,
    is_patched,
    get_patched_loggers
)

__all__ = [
    'ColoredStreamHandler',
    'ColoredConsoleHandler',
    'ColoredFileHandler',
    'SmartColorHandler',
    'DualOutputHandler',
    'ColoredFormatter',
    'MinimalColoredFormatter',
    'DetailedColoredFormatter',
    'JSONColoredFormatter',
    'LoggingPatcher',
    'patch_logging',
    'unpatch_logging',
    'patch_logger',
    'is_patched',
    'get_patched_loggers'
] 