import logging
import sys
from .formatter import ColorFormatter
from ..utils.terminal import is_terminal_supports_color
from ..utils.compatibility import ensure_color_support

_original_formatter_class = None
_original_handler_emit = None
_original_stream_handler_emit = None
_patched = False

def _get_color_formatter_class():
    class PatchedFormatter(logging.Formatter):
        def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
            super().__init__(fmt, datefmt, style, validate, defaults=defaults)
            self._color_formatter = ColorFormatter(fmt, datefmt, style, validate, defaults=defaults)
        
        def format(self, record):
            if is_terminal_supports_color():
                return self._color_formatter.format(record)
            return super().format(record)
    
    return PatchedFormatter

def _patched_handler_emit(self, record):
    if hasattr(self, 'stream') and self.stream in (sys.stdout, sys.stderr):
        if not hasattr(self.formatter, '_color_formatter'):
            if is_terminal_supports_color():
                original_format = self.formatter._fmt if hasattr(self.formatter, '_fmt') else None
                original_datefmt = self.formatter.datefmt if hasattr(self.formatter, 'datefmt') else None
                original_style = getattr(self.formatter, '_style', '%')
                
                if hasattr(original_style, '_fmt'):
                    original_style = original_style._fmt
                elif hasattr(original_style, 'default_format'):
                    original_style = '%'
                else:
                    original_style = '%'
                
                self.formatter = ColorFormatter(original_format, original_datefmt, original_style)
    
    return _original_handler_emit(self, record)

def patch_logging():
    global _original_formatter_class, _original_handler_emit, _patched
    
    if _patched:
        return
    
    try:
        _original_formatter_class = logging.Formatter
        _original_handler_emit = logging.Handler.emit
        
        logging.Formatter = _get_color_formatter_class()
        logging.Handler.emit = _patched_handler_emit
        
        _patched = True
        
        if is_terminal_supports_color():
            ensure_color_support()
        
    except Exception:
        _patched = False

def unpatch_logging():
    global _original_formatter_class, _original_handler_emit, _patched
    
    if not _patched:
        return
    
    try:
        if _original_formatter_class:
            logging.Formatter = _original_formatter_class
        
        if _original_handler_emit:
            logging.Handler.emit = _original_handler_emit
        
        _patched = False
        
    except Exception:
        pass

def is_patched():
    return _patched 