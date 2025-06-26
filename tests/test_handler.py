import unittest
import sys
import logging
from io import StringIO
from unittest.mock import patch
from smartlogger.core.handler import ColorHandler
from smartlogger.core.formatter import ColorFormatter

class TestColorHandler(unittest.TestCase):
    
    def setUp(self):
        self.stream = StringIO()
        self.handler = ColorHandler(self.stream)
        self.record = logging.LogRecord(
            name='test',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
    
    def test_handler_initialization(self):
        handler = ColorHandler()
        self.assertIsInstance(handler, logging.StreamHandler)
    
    def test_handler_with_custom_stream(self):
        stream = StringIO()
        handler = ColorHandler(stream)
        self.assertEqual(handler.stream, stream)
    
    @patch('smartlogger.utils.terminal.is_terminal_supports_color', return_value=True)
    def test_handler_uses_color_formatter_when_supported(self, mock_supports_color):
        handler = ColorHandler()
        self.assertIsInstance(handler.formatter, ColorFormatter)
    
    @patch('smartlogger.utils.terminal.is_terminal_supports_color', return_value=False)
    def test_handler_uses_standard_formatter_when_not_supported(self, mock_supports_color):
        handler = ColorHandler()
        self.assertIsInstance(handler.formatter, ColorFormatter)
    
    def test_emit_functionality(self):
        self.handler.emit(self.record)
        output = self.stream.getvalue()
        self.assertIn('Test message', output)

if __name__ == '__main__':
    unittest.main() 