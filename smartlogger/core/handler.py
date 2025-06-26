# Custom handlers for colored logging 

import sys
import logging
from typing import Optional, TextIO, Any

from ..config.colors import get_default_scheme, ColorScheme
from ..utils.terminal import supports_colors, stream_supports_color
from ..utils.compatibility import (
    safe_getattr,
    safe_hasattr,
    get_stream_encoding
)
from ..exceptions import HandlerCreationError
from .formatter import ColoredFormatter


class ColoredStreamHandler(logging.StreamHandler):
    def __init__(
        self, 
        stream: Optional[TextIO] = None,
        color_scheme: Optional[ColorScheme] = None,
        force_color: bool = False
    ):
        stream = stream or sys.stderr
        super().__init__(stream)
        
        self._color_scheme = color_scheme or get_default_scheme()
        self._force_color = force_color
        self._supports_color = self._check_color_support()
        
        if not self.formatter:
            self.setFormatter(ColoredFormatter(color_scheme=self._color_scheme))
    
    def _check_color_support(self) -> bool:
        if self._force_color:
            return True
        
        if not supports_colors():
            return False
        
        if not stream_supports_color(self.stream):
            return False
        
        return True
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            if not self._supports_color and hasattr(self.formatter, 'disable_colors'):
                self.formatter.disable_colors()
            elif self._supports_color and hasattr(self.formatter, 'enable_colors'):
                self.formatter.enable_colors()
            
            super().emit(record)
            
        except Exception:
            self.handleError(record)
    
    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        self._color_scheme = color_scheme
        if hasattr(self.formatter, 'set_color_scheme'):
            self.formatter.set_color_scheme(color_scheme)
    
    def enable_colors(self) -> None:
        self._force_color = True
        self._supports_color = True
        if hasattr(self.formatter, 'enable_colors'):
            self.formatter.enable_colors()
    
    def disable_colors(self) -> None:
        self._force_color = False
        self._supports_color = False
        if hasattr(self.formatter, 'disable_colors'):
            self.formatter.disable_colors()
    
    @property
    def colors_enabled(self) -> bool:
        return self._supports_color


class ColoredConsoleHandler(ColoredStreamHandler):
    def __init__(
        self, 
        color_scheme: Optional[ColorScheme] = None,
        force_color: bool = False,
        use_stderr: bool = True
    ):
        stream = sys.stderr if use_stderr else sys.stdout
        super().__init__(stream, color_scheme, force_color)


class ColoredFileHandler(logging.FileHandler):
    def __init__(
        self,
        filename: str,
        mode: str = 'a',
        encoding: Optional[str] = None,
        delay: bool = False,
        color_scheme: Optional[ColorScheme] = None,
        force_color: bool = False
    ):
        super().__init__(filename, mode, encoding, delay)
        
        self._color_scheme = color_scheme or get_default_scheme()
        self._force_color = force_color
        
        if not self.formatter:
            self.setFormatter(ColoredFormatter(color_scheme=self._color_scheme))
        
        if not force_color and hasattr(self.formatter, 'disable_colors'):
            self.formatter.disable_colors()
    
    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        self._color_scheme = color_scheme
        if hasattr(self.formatter, 'set_color_scheme'):
            self.formatter.set_color_scheme(color_scheme)
    
    def enable_colors(self) -> None:
        self._force_color = True
        if hasattr(self.formatter, 'enable_colors'):
            self.formatter.enable_colors()
    
    def disable_colors(self) -> None:
        self._force_color = False
        if hasattr(self.formatter, 'disable_colors'):
            self.formatter.disable_colors()


class SmartColorHandler(ColoredStreamHandler):
    def __init__(
        self,
        stream: Optional[TextIO] = None,
        color_scheme: Optional[ColorScheme] = None,
        fallback_handler: Optional[logging.Handler] = None
    ):
        super().__init__(stream, color_scheme)
        self._fallback_handler = fallback_handler
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            super().emit(record)
        except Exception:
            if self._fallback_handler:
                try:
                    self._fallback_handler.emit(record)
                except Exception:
                    self.handleError(record)
            else:
                self.handleError(record)


class DualOutputHandler(logging.Handler):
    def __init__(
        self,
        stdout_handler: Optional[logging.Handler] = None,
        stderr_handler: Optional[logging.Handler] = None,
        error_levels: Optional[set] = None
    ):
        super().__init__()
        
        self._stdout_handler = stdout_handler or ColoredConsoleHandler(use_stderr=False)
        self._stderr_handler = stderr_handler or ColoredConsoleHandler(use_stderr=True)
        self._error_levels = error_levels or {logging.WARNING, logging.ERROR, logging.CRITICAL}
    
    def emit(self, record: logging.LogRecord) -> None:
        try:
            if record.levelno in self._error_levels:
                self._stderr_handler.emit(record)
            else:
                self._stdout_handler.emit(record)
        except Exception:
            self.handleError(record)
    
    def setFormatter(self, formatter: logging.Formatter) -> None:
        self._stdout_handler.setFormatter(formatter)
        self._stderr_handler.setFormatter(formatter)
    
    def setLevel(self, level: int) -> None:
        super().setLevel(level)
        self._stdout_handler.setLevel(level)
        self._stderr_handler.setLevel(level) 