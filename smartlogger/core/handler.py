import logging
import sys
from .formatter import ColorFormatter
from ..utils.terminal import is_terminal_supports_color

class ColorHandler(logging.StreamHandler):
    def __init__(self, stream=None):
        super().__init__(stream or sys.stderr)
        self.setFormatter(ColorFormatter())
    
    def emit(self, record):
        try:
            super().emit(record)
        except Exception:
            self.handleError(record) 