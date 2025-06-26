import unittest
import logging
from unittest.mock import patch, MagicMock
from smartlogger.core.formatter import ColorFormatter
from smartlogger.config.colors import Colors

class TestColorFormatter(unittest.TestCase):
    
    def setUp(self):
        self.formatter = ColorFormatter()
        self.record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
    
    def test_formatter_initialization(self):
        formatter = ColorFormatter()
        self.assertTrue(hasattr(formatter, 'format'))
    
    @patch('smartlogger.utils.terminal.is_terminal_supports_color', return_value=True)
    def test_format_with_colors_enabled(self, mock_supports_color):
        formatter = ColorFormatter()
        formatted = formatter.format(self.record)
        self.assertIn('INFO', formatted)
    
    @patch('smartlogger.utils.terminal.is_terminal_supports_color', return_value=False)
    def test_format_with_colors_disabled(self, mock_supports_color):
        formatter = ColorFormatter()
        formatted = formatter.format(self.record)
        self.assertIn('INFO', formatted)
    
    def test_enable_disable_colors(self):
        formatter = ColorFormatter()
        formatter.disable_colors()
        self.assertFalse(formatter.color_enabled)
        
        formatter.enable_colors()
        self.assertTrue(formatter.color_enabled)
    
    def test_level_name_restoration(self):
        original_levelname = self.record.levelname
        formatter = ColorFormatter()
        formatter.format(self.record)
        self.assertEqual(self.record.levelname, original_levelname)

if __name__ == '__main__':
    unittest.main() 