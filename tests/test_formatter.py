# Tests for custom formatters 

import unittest
import logging
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

from smartlogger.core.formatter import (
    ColoredFormatter, 
    MinimalColoredFormatter,
    DetailedColoredFormatter,
    JSONColoredFormatter
)
from smartlogger.config.colors import ColorScheme, ANSIColors
from smartlogger.exceptions import FormatterError


class TestColoredFormatter(unittest.TestCase):
    
    def setUp(self):
        self.color_scheme = ColorScheme()
        self.formatter = ColoredFormatter(color_scheme=self.color_scheme)
        self.record = logging.LogRecord(
            name='test_logger',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
    
    def test_init_with_custom_color_scheme(self):
        custom_scheme = ColorScheme({'INFO': ANSIColors.RED})
        formatter = ColoredFormatter(color_scheme=custom_scheme)
        self.assertEqual(formatter._color_scheme, custom_scheme)
    
    def test_init_with_default_color_scheme(self):
        formatter = ColoredFormatter()
        self.assertIsNotNone(formatter._color_scheme)
    
    def test_format_with_colors_enabled(self):
        self.color_scheme.enable()
        formatted = self.formatter.format(self.record)
        
        self.assertIn(ANSIColors.GREEN, formatted)
        self.assertIn(ANSIColors.RESET, formatted)
        self.assertIn('Test message', formatted)
    
    def test_format_with_colors_disabled(self):
        self.color_scheme.disable()
        formatted = self.formatter.format(self.record)
        
        self.assertNotIn(ANSIColors.GREEN, formatted)
        self.assertNotIn(ANSIColors.RESET, formatted)
        self.assertIn('Test message', formatted)
    
    def test_format_preserves_original_levelname(self):
        original_levelname = self.record.levelname
        self.formatter.format(self.record)
        self.assertEqual(self.record.levelname, original_levelname)
    
    def test_format_different_log_levels(self):
        levels = [
            (logging.DEBUG, ANSIColors.BRIGHT_BLUE),
            (logging.INFO, ANSIColors.GREEN),
            (logging.WARNING, ANSIColors.YELLOW),
            (logging.ERROR, ANSIColors.RED),
            (logging.CRITICAL, ANSIColors.BOLD + ANSIColors.RED)
        ]
        
        for level, expected_color in levels:
            record = logging.LogRecord(
                name='test', level=level, pathname='test.py', lineno=1,
                msg='Test', args=(), exc_info=None
            )
            formatted = self.formatter.format(record)
            if self.color_scheme.enabled:
                self.assertIn(expected_color, formatted)
    
    def test_format_exception_handling(self):
        with patch('smartlogger.core.formatter.get_record_levelname') as mock_get_level:
            mock_get_level.side_effect = Exception("Test exception")
            
            formatted = self.formatter.format(self.record)
            self.assertIn('[FORMATTER ERROR]', formatted)
            self.assertIn('Test message', formatted)
    
    def test_format_critical_exception_handling(self):
        with patch('smartlogger.core.formatter.get_record_levelname') as mock_get_level:
            with patch('smartlogger.core.formatter.get_record_message') as mock_get_msg:
                mock_get_level.side_effect = Exception("Level error")
                mock_get_msg.side_effect = Exception("Message error")
                
                formatted = self.formatter.format(self.record)
                self.assertIn('[CRITICAL FORMATTER ERROR]', formatted)
    
    def test_set_color_scheme(self):
        new_scheme = ColorScheme({'INFO': ANSIColors.BLUE})
        self.formatter.set_color_scheme(new_scheme)
        self.assertEqual(self.formatter._color_scheme, new_scheme)
    
    def test_get_color_scheme(self):
        scheme = self.formatter.get_color_scheme()
        self.assertEqual(scheme, self.color_scheme)
    
    def test_enable_colors(self):
        self.formatter.enable_colors()
        self.assertTrue(self.formatter.colors_enabled)
    
    def test_disable_colors(self):
        self.formatter.disable_colors()
        self.assertFalse(self.formatter.colors_enabled)
    
    def test_colors_enabled_property(self):
        self.formatter.enable_colors()
        self.assertTrue(self.formatter.colors_enabled)
        
        self.formatter.disable_colors()
        self.assertFalse(self.formatter.colors_enabled)


class TestMinimalColoredFormatter(unittest.TestCase):
    
    def setUp(self):
        self.formatter = MinimalColoredFormatter()
        self.record = logging.LogRecord(
            name='test_logger',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
    
    def test_format_structure(self):
        formatted = self.formatter.format(self.record)
        self.assertIn('INFO', formatted)
        self.assertIn('Test message', formatted)
        self.assertNotIn('test_logger', formatted)
        self.assertNotIn('test.py', formatted)
        
    def test_inherits_from_colored_formatter(self):
        self.assertIsInstance(self.formatter, ColoredFormatter)


class TestDetailedColoredFormatter(unittest.TestCase):
    
    def setUp(self):
        self.formatter = DetailedColoredFormatter()
        self.record = logging.LogRecord(
            name='test_logger',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
    
    def test_format_structure(self):
        formatted = self.formatter.format(self.record)
        self.assertIn('INFO', formatted)
        self.assertIn('Test message', formatted)
        self.assertIn('test_logger', formatted)
        self.assertRegex(formatted, r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}')
    
    def test_inherits_from_colored_formatter(self):
        self.assertIsInstance(self.formatter, ColoredFormatter)


class TestJSONColoredFormatter(unittest.TestCase):
    
    def setUp(self):
        self.formatter = JSONColoredFormatter()
        self.record = logging.LogRecord(
            name='test_logger',
            level=logging.INFO,
            pathname='test.py',
            lineno=1,
            msg='Test message',
            args=(),
            exc_info=None
        )
    
    def test_format_json_structure(self):
        formatted = self.formatter.format(self.record)
        
        import json
        try:
            data = json.loads(formatted.replace(ANSIColors.GREEN, '').replace(ANSIColors.RESET, ''))
            self.assertIn('timestamp', data)
            self.assertIn('level', data)
            self.assertIn('logger', data)
            self.assertIn('message', data)
            self.assertEqual(data['level'], 'INFO')
            self.assertEqual(data['logger'], 'test_logger')
            self.assertEqual(data['message'], 'Test message')
        except json.JSONDecodeError:
            self.fail("Output is not valid JSON")
    
    def test_format_with_colors(self):
        self.formatter.enable_colors()
        formatted = self.formatter.format(self.record)
        
        if self.formatter._color_scheme.enabled:
            self.assertIn(ANSIColors.GREEN, formatted)
            self.assertIn(ANSIColors.RESET, formatted)
    
    def test_format_exception_fallback(self):
        with patch('json.dumps') as mock_dumps:
            mock_dumps.side_effect = Exception("JSON error")
            
            formatted = self.formatter.format(self.record)
            self.assertIn('Test message', formatted)
    
    def test_inherits_from_colored_formatter(self):
        self.assertIsInstance(self.formatter, ColoredFormatter)


class TestFormatterIntegration(unittest.TestCase):
    
    def test_formatter_with_handler(self):
        handler = logging.StreamHandler(StringIO())
        formatter = ColoredFormatter()
        handler.setFormatter(formatter)
        
        logger = logging.getLogger('test_integration')
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        
        logger.info('Integration test message')
        
        output = handler.stream.getvalue()
        self.assertIn('Integration test message', output)
    
    def test_multiple_formatters_same_record(self):
        record = logging.LogRecord(
            name='test', level=logging.WARNING, pathname='test.py', lineno=1,
            msg='Warning message', args=(), exc_info=None
        )
        
        minimal = MinimalColoredFormatter()
        detailed = DetailedColoredFormatter()
        json_fmt = JSONColoredFormatter()
        
        minimal_output = minimal.format(record)
        detailed_output = detailed.format(record)
        json_output = json_fmt.format(record)
        
        self.assertIn('Warning message', minimal_output)
        self.assertIn('Warning message', detailed_output)
        self.assertIn('Warning message', json_output)
        
        self.assertNotEqual(minimal_output, detailed_output)
        self.assertNotEqual(detailed_output, json_output)


if __name__ == '__main__':
    unittest.main() 