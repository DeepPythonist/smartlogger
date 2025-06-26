# Compatibility utilities for different Python versions 

import sys
import logging
from typing import Any, Optional, Union, Dict


PY_VERSION = sys.version_info
PY37_PLUS = PY_VERSION >= (3, 7)
PY38_PLUS = PY_VERSION >= (3, 8)
PY39_PLUS = PY_VERSION >= (3, 9)
PY310_PLUS = PY_VERSION >= (3, 10)
PY311_PLUS = PY_VERSION >= (3, 11)


def get_python_version() -> str:
    return f"{PY_VERSION.major}.{PY_VERSION.minor}.{PY_VERSION.micro}"


def is_python_version_supported() -> bool:
    return PY37_PLUS


def safe_getattr(obj: Any, name: str, default: Any = None) -> Any:
    try:
        return getattr(obj, name, default)
    except (AttributeError, TypeError):
        return default


def safe_hasattr(obj: Any, name: str) -> bool:
    try:
        return hasattr(obj, name)
    except (AttributeError, TypeError):
        return False


def safe_isinstance(obj: Any, class_or_tuple: Union[type, tuple]) -> bool:
    try:
        return isinstance(obj, class_or_tuple)
    except (TypeError, AttributeError):
        return False


def safe_callable(obj: Any) -> bool:
    try:
        return callable(obj)
    except (TypeError, AttributeError):
        return False


def get_logging_level_name(level: int) -> str:
    try:
        if PY38_PLUS:
            return logging.getLevelName(level)
        else:
            level_names = {
                logging.DEBUG: 'DEBUG',
                logging.INFO: 'INFO',
                logging.WARNING: 'WARNING',
                logging.ERROR: 'ERROR',
                logging.CRITICAL: 'CRITICAL'
            }
            return level_names.get(level, f'Level {level}')
    except Exception:
        return f'Level {level}'


def get_stream_encoding(stream: Any) -> str:
    try:
        encoding = safe_getattr(stream, 'encoding')
        if encoding:
            return encoding
        return 'utf-8'
    except Exception:
        return 'utf-8'


def stream_supports_color(stream: Any) -> bool:
    try:
        if not safe_hasattr(stream, 'isatty'):
            return False
        
        if not safe_callable(stream.isatty):
            return False
        
        return stream.isatty()
    except Exception:
        return False


def get_logging_handlers(logger: logging.Logger) -> list:
    try:
        return list(logger.handlers)
    except (AttributeError, TypeError):
        return []


def get_root_logger() -> logging.Logger:
    try:
        return logging.getLogger()
    except Exception:
        return logging.root


def create_logger(name: str) -> logging.Logger:
    try:
        return logging.getLogger(name)
    except Exception:
        return logging.root


def get_logger_level(logger: logging.Logger) -> int:
    try:
        return logger.level
    except (AttributeError, TypeError):
        return logging.NOTSET


def set_logger_level(logger: logging.Logger, level: int) -> bool:
    try:
        logger.setLevel(level)
        return True
    except Exception:
        return False


def add_handler_to_logger(logger: logging.Logger, handler: logging.Handler) -> bool:
    try:
        logger.addHandler(handler)
        return True
    except Exception:
        return False


def remove_handler_from_logger(logger: logging.Logger, handler: logging.Handler) -> bool:
    try:
        logger.removeHandler(handler)
        return True
    except Exception:
        return False


def format_record_safe(formatter: logging.Formatter, record: logging.LogRecord) -> str:
    try:
        return formatter.format(record)
    except Exception as e:
        return f"Failed to format log record: {e}"


def get_record_levelname(record: logging.LogRecord) -> str:
    try:
        return record.levelname
    except (AttributeError, TypeError):
        return get_logging_level_name(getattr(record, 'levelno', logging.INFO))


def get_record_message(record: logging.LogRecord) -> str:
    try:
        if safe_hasattr(record, 'getMessage'):
            return record.getMessage()
        return str(getattr(record, 'msg', ''))
    except Exception:
        return str(getattr(record, 'msg', ''))


class CompatibilityError(Exception):
    pass


def check_compatibility() -> None:
    if not is_python_version_supported():
        raise CompatibilityError(
            f"Python {get_python_version()} is not supported. "
            "SmartLogger requires Python 3.7 or higher."
        ) 