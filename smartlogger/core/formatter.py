# Custom formatters for colored logging 
import logging
from typing import Optional

from ..config.colors import get_default_scheme, ColorScheme
from ..utils.compatibility import (
    get_record_levelname, 
    get_record_message,
    format_record_safe
)
from ..exceptions import FormatterError


class ColoredFormatter(logging.Formatter):
    def __init__(
        self, 
        fmt: Optional[str] = None, 
        datefmt: Optional[str] = None,
        style: str = '%',
        color_scheme: Optional[ColorScheme] = None
    ):
        super().__init__(fmt, datefmt, style)
        self._color_scheme = color_scheme or get_default_scheme()
        self._original_format = fmt or self._fmt
    
    def format(self, record: logging.LogRecord) -> str:
        try:
            level_name = get_record_levelname(record)
            color_code = self._color_scheme.get_color(level_name)
            reset_code = self._color_scheme.get_reset()
            
            if color_code and self._color_scheme.enabled:
                colored_levelname = f"{color_code}{level_name}{reset_code}"
                
                original_levelname = record.levelname
                record.levelname = colored_levelname
                
                try:
                    formatted_message = super().format(record)
                finally:
                    record.levelname = original_levelname
                
                return formatted_message
            else:
                return super().format(record)
                
        except Exception as e:
            try:
                fallback_msg = f"[FORMATTER ERROR] {get_record_message(record)}"
                return fallback_msg
            except Exception:
                return f"[CRITICAL FORMATTER ERROR] {str(e)}"
    
    def set_color_scheme(self, color_scheme: ColorScheme) -> None:
        self._color_scheme = color_scheme
    
    def get_color_scheme(self) -> ColorScheme:
        return self._color_scheme
    
    def enable_colors(self) -> None:
        self._color_scheme.enable()
    
    def disable_colors(self) -> None:
        self._color_scheme.disable()
    
    @property
    def colors_enabled(self) -> bool:
        return self._color_scheme.enabled


class MinimalColoredFormatter(ColoredFormatter):
    def __init__(
        self, 
        color_scheme: Optional[ColorScheme] = None
    ):
        super().__init__(
            fmt='%(levelname)s: %(message)s',
            color_scheme=color_scheme
        )


class DetailedColoredFormatter(ColoredFormatter):
    def __init__(
        self, 
        color_scheme: Optional[ColorScheme] = None
    ):
        super().__init__(
            fmt='%(asctime)s [%(name)s] %(levelname)s: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            color_scheme=color_scheme
        )


class JSONColoredFormatter(ColoredFormatter):
    def format(self, record: logging.LogRecord) -> str:
        try:
            import json
            
            level_name = get_record_levelname(record)
            color_code = self._color_scheme.get_color(level_name)
            reset_code = self._color_scheme.get_reset()
            
            log_data = {
                'timestamp': self.formatTime(record),
                'level': level_name,
                'logger': record.name,
                'message': get_record_message(record),
                'module': getattr(record, 'module', ''),
                'function': getattr(record, 'funcName', ''),
                'line': getattr(record, 'lineno', 0)
            }
            
            json_str = json.dumps(log_data, ensure_ascii=False)
            
            if color_code and self._color_scheme.enabled:
                return f"{color_code}{json_str}{reset_code}"
            else:
                return json_str
                
        except Exception as e:
            return super().format(record) 