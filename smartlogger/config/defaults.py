# Default configurations and settings 
import logging
from typing import Dict, Any


DEFAULT_LOG_LEVEL = logging.INFO

DEFAULT_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'

LEVEL_NAMES = {
    logging.DEBUG: 'DEBUG',
    logging.INFO: 'INFO',
    logging.WARNING: 'WARNING',
    logging.ERROR: 'ERROR',
    logging.CRITICAL: 'CRITICAL'
}

LEVEL_NAME_TO_NUMBER = {
    'DEBUG': logging.DEBUG,
    'INFO': logging.INFO,
    'WARNING': logging.WARNING,
    'ERROR': logging.ERROR,
    'CRITICAL': logging.CRITICAL
}

DEFAULT_HANDLER_CONFIG = {
    'class': 'smartlogger.core.handler.ColoredStreamHandler',
    'formatter': 'colored',
    'stream': 'sys.stdout'
}

DEFAULT_FORMATTER_CONFIG = {
    'class': 'smartlogger.core.formatter.ColoredFormatter',
    'format': DEFAULT_FORMAT,
    'datefmt': DEFAULT_DATE_FORMAT
}

DEFAULT_LOGGER_CONFIG = {
    'handlers': ['colored_console'],
    'level': DEFAULT_LOG_LEVEL,
    'propagate': True
}

PATCHING_CONFIG = {
    'auto_patch': True,
    'patch_root_logger': True,
    'preserve_existing_handlers': True,
    'add_colored_handler': True
}

TERMINAL_CONFIG = {
    'detect_capability': True,
    'fallback_on_error': True,
    'respect_no_color': True,
    'force_color_env_var': 'FORCE_COLOR',
    'no_color_env_var': 'NO_COLOR'
}

PERFORMANCE_CONFIG = {
    'lazy_import': True,
    'cache_color_detection': True,
    'minimal_overhead': True
}


def get_config() -> Dict[str, Any]:
    return {
        'log_level': DEFAULT_LOG_LEVEL,
        'format': DEFAULT_FORMAT,
        'date_format': DEFAULT_DATE_FORMAT,
        'handler': DEFAULT_HANDLER_CONFIG,
        'formatter': DEFAULT_FORMATTER_CONFIG,
        'logger': DEFAULT_LOGGER_CONFIG,
        'patching': PATCHING_CONFIG,
        'terminal': TERMINAL_CONFIG,
        'performance': PERFORMANCE_CONFIG
    } 