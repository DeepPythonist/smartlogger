__version__ = "1.3.0"
__author__ = "Mohammad Rasol Esfandiari"
__email__ = "mrasolesfandiari@gmail.com"
__license__ = "MIT"

from .core.formatter import ColorFormatter
from .core.handler import ColorHandler
from .config.colors import Colors
from .utils.terminal import is_terminal_supports_color 