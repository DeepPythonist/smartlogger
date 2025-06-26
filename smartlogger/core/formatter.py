import logging
from ..config.colors import Colors
from ..config.defaults import DEFAULT_FORMAT, DEFAULT_DATE_FORMAT
from ..utils.terminal import is_terminal_supports_color
from ..utils.compatibility import ensure_color_support

class ColorFormatter(logging.Formatter):
    def __init__(self, fmt=None, datefmt=None, style='%', validate=True, *, defaults=None):
        super().__init__(fmt or DEFAULT_FORMAT, datefmt or DEFAULT_DATE_FORMAT, style, validate, defaults=defaults)
        self.color_enabled = is_terminal_supports_color()
        if self.color_enabled:
            ensure_color_support()
    
    def format(self, record):
        if not self.color_enabled:
            return super().format(record)
        
        original_levelname = record.levelname
        color = Colors.get_color_for_level(record.levelname)
        
        if color:
            record.levelname = Colors.colorize(record.levelname, color)
        
        try:
            formatted = super().format(record)
        finally:
            record.levelname = original_levelname
        
        return formatted
    
    def enable_colors(self):
        self.color_enabled = True
        ensure_color_support()
    
    def disable_colors(self):
        self.color_enabled = False 