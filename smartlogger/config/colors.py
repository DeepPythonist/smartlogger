import sys
import os

class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    
    BRIGHT_BLACK = '\033[90m'
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'
    
    @classmethod
    def get_color_for_level(cls, level_name):
        level_colors = {
            'DEBUG': cls.BLUE,
            'INFO': cls.GREEN,
            'WARNING': cls.YELLOW,
            'ERROR': cls.RED,
            'CRITICAL': cls.BRIGHT_RED + cls.BOLD
        }
        return level_colors.get(level_name, cls.RESET)
    
    @classmethod
    def colorize(cls, text, color):
        return f"{color}{text}{cls.RESET}"
    
    @classmethod
    def strip_colors(cls, text):
        import re
        ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
        return ansi_escape.sub('', text) 