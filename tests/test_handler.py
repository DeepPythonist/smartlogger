# Tests for custom handlers 

import unittest
import logging
import sys
from io import StringIO
from unittest.mock import Mock, patch, MagicMock

from smartlogger.core.handler import (
    ColoredStreamHandler,
    ColoredConsoleHandler,
    ColoredFileHandler,
    SmartColorHandler,
    DualOutputHandler
)
from smartlogger.config.colors import ColorScheme, ANSIColors
from smartlogger.core.formatter import ColoredFormatter
from smartlogger.exceptions import HandlerCreationError


class TestColoredStreamHandler(unittest.TestCase):
    
    def setUp(self):
        self.stream = StringIO()
        self.color_scheme = ColorScheme()
        self.handler = ColoredStreamHandler(self.stream, self.color_scheme)
    
    def test_init_default_stream(self):
        handler = ColoredStreamHandler()
        self.assertEqual(handler.stream, sys.stderr)
    
    def test_init_custom_stream(self):
        custom_stream = StringIO()
        handler = ColoredStreamHandler(custom_stream)
        self.assertEqual(handler.stream, custom_stream)
    
    def test_init_sets_formatter(self):
        handler = ColoredStreamHandler(self.stream)
        self.assertIsInstance(handler.formatter, ColoredFormatter)
    
    @patch('smartlogger.core.handler.supports_colors')
    @patch('smartlogger.core.handler.stream_supports_color')
    def test_check_color_support_true(self, mock_stream_supports, mock_supports):
        mock_supports.return_value = True
        mock_stream_supports.return_value = True
        
        handler = ColoredStreamHandler(self.stream)
        self.assertTrue(handler._supports_color)
    
    @patch('smartlogger.core.handler.supports_colors')
    def test_check_color_support_false_no_terminal_support(self, mock_supports):
        mock_supports.return_value = False
        
        handler = ColoredStreamHandler(self.stream)
        self.assertFalse(handler._supports_color)
    
    def test_force_color_overrides_detection(self):
        handler = ColoredStreamHandler(self.stream, force_color=True)
        self.assertTrue(handler._supports_color)
    
    def test_emit_enables_colors_when_supported(self):
        self.handler._supports_color = True
        mock_formatter = Mock()
        mock_formatter.enable_colors = Mock()
        self.handler.formatter = mock_formatter
        
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Test message', (), None
        )
        
        self.handler.emit(record)
        mock_formatter.enable_colors.assert_called_once()
    
    def test_emit_disables_colors_when_not_supported(self):
        self.handler._supports_color = False
        mock_formatter = Mock()
        mock_formatter.disable_colors = Mock()
        self.handler.formatter = mock_formatter
        
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Test message', (), None
        )
        
        self.handler.emit(record)
        mock_formatter.disable_colors.assert_called_once()
    
    def test_set_color_scheme(self):
        new_scheme = ColorScheme({'INFO': ANSIColors.BLUE})
        mock_formatter = Mock()
        mock_formatter.set_color_scheme = Mock()
        self.handler.formatter = mock_formatter
        
        self.handler.set_color_scheme(new_scheme)
        
        self.assertEqual(self.handler._color_scheme, new_scheme)
        mock_formatter.set_color_scheme.assert_called_once_with(new_scheme)
    
    def test_enable_colors(self):
        mock_formatter = Mock()
        mock_formatter.enable_colors = Mock()
        self.handler.formatter = mock_formatter
        
        self.handler.enable_colors()
        
        self.assertTrue(self.handler._force_color)
        self.assertTrue(self.handler._supports_color)
        mock_formatter.enable_colors.assert_called_once()
    
    def test_disable_colors(self):
        mock_formatter = Mock()
        mock_formatter.disable_colors = Mock()
        self.handler.formatter = mock_formatter
        
        self.handler.disable_colors()
        
        self.assertFalse(self.handler._force_color)
        self.assertFalse(self.handler._supports_color)
        mock_formatter.disable_colors.assert_called_once()
    
    def test_colors_enabled_property(self):
        self.handler._supports_color = True
        self.assertTrue(self.handler.colors_enabled)
        
        self.handler._supports_color = False
        self.assertFalse(self.handler.colors_enabled)


class TestColoredConsoleHandler(unittest.TestCase):
    
    def test_init_default_stderr(self):
        handler = ColoredConsoleHandler()
        self.assertEqual(handler.stream, sys.stderr)
    
    def test_init_stdout_option(self):
        handler = ColoredConsoleHandler(use_stderr=False)
        self.assertEqual(handler.stream, sys.stdout)
    
    def test_inherits_from_colored_stream_handler(self):
        handler = ColoredConsoleHandler()
        self.assertIsInstance(handler, ColoredStreamHandler)


class TestColoredFileHandler(unittest.TestCase):
    
    def setUp(self):
        self.test_file = 'test_log.txt'
    
    def tearDown(self):
        import os
        try:
            os.remove(self.test_file)
        except FileNotFoundError:
            pass
    
    def test_init_with_default_params(self):
        handler = ColoredFileHandler(self.test_file)
        self.assertEqual(handler.baseFilename, handler.baseFilename)
        self.assertIsInstance(handler.formatter, ColoredFormatter)
    
    def test_init_disables_colors_by_default(self):
        with patch.object(ColoredFormatter, 'disable_colors') as mock_disable:
            handler = ColoredFileHandler(self.test_file)
            mock_disable.assert_called_once()
    
    def test_init_with_force_color(self):
        with patch.object(ColoredFormatter, 'disable_colors') as mock_disable:
            handler = ColoredFileHandler(self.test_file, force_color=True)
            mock_disable.assert_not_called()
    
    def test_set_color_scheme(self):
        handler = ColoredFileHandler(self.test_file)
        new_scheme = ColorScheme({'INFO': ANSIColors.BLUE})
        
        with patch.object(handler.formatter, 'set_color_scheme') as mock_set:
            handler.set_color_scheme(new_scheme)
            mock_set.assert_called_once_with(new_scheme)
    
    def test_enable_colors(self):
        handler = ColoredFileHandler(self.test_file)
        
        with patch.object(handler.formatter, 'enable_colors') as mock_enable:
            handler.enable_colors()
            mock_enable.assert_called_once()
            self.assertTrue(handler._force_color)
    
    def test_disable_colors(self):
        handler = ColoredFileHandler(self.test_file)
        
        with patch.object(handler.formatter, 'disable_colors') as mock_disable:
            handler.disable_colors()
            self.assertFalse(handler._force_color)


class TestSmartColorHandler(unittest.TestCase):
    
    def setUp(self):
        self.stream = StringIO()
        self.fallback_handler = Mock(spec=logging.Handler)
        self.handler = SmartColorHandler(
            self.stream, 
            fallback_handler=self.fallback_handler
        )
    
    def test_inherits_from_colored_stream_handler(self):
        self.assertIsInstance(self.handler, ColoredStreamHandler)
    
    def test_emit_success(self):
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Test message', (), None
        )
        
        with patch.object(ColoredStreamHandler, 'emit') as mock_super_emit:
            self.handler.emit(record)
            mock_super_emit.assert_called_once_with(record)
    
    def test_emit_fallback_on_exception(self):
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Test message', (), None
        )
        
        with patch.object(ColoredStreamHandler, 'emit') as mock_super_emit:
            mock_super_emit.side_effect = Exception("Emit failed")
            
            self.handler.emit(record)
            
            self.fallback_handler.emit.assert_called_once_with(record)
    
    def test_emit_handle_error_when_no_fallback(self):
        handler = SmartColorHandler(self.stream)
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Test message', (), None
        )
        
        with patch.object(ColoredStreamHandler, 'emit') as mock_super_emit:
            with patch.object(handler, 'handleError') as mock_handle_error:
                mock_super_emit.side_effect = Exception("Emit failed")
                
                handler.emit(record)
                mock_handle_error.assert_called_once_with(record)
    
    def test_emit_handle_error_when_fallback_fails(self):
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Test message', (), None
        )
        
        with patch.object(ColoredStreamHandler, 'emit') as mock_super_emit:
            with patch.object(self.handler, 'handleError') as mock_handle_error:
                mock_super_emit.side_effect = Exception("Emit failed")
                self.fallback_handler.emit.side_effect = Exception("Fallback failed")
                
                self.handler.emit(record)
                mock_handle_error.assert_called_once_with(record)


class TestDualOutputHandler(unittest.TestCase):
    
    def setUp(self):
        self.stdout_handler = Mock(spec=logging.Handler)
        self.stderr_handler = Mock(spec=logging.Handler)
        self.handler = DualOutputHandler(
            self.stdout_handler,
            self.stderr_handler
        )
    
    def test_init_with_default_handlers(self):
        handler = DualOutputHandler()
        self.assertIsInstance(handler._stdout_handler, ColoredConsoleHandler)
        self.assertIsInstance(handler._stderr_handler, ColoredConsoleHandler)
    
    def test_emit_info_to_stdout(self):
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Info message', (), None
        )
        
        self.handler.emit(record)
        
        self.stdout_handler.emit.assert_called_once_with(record)
        self.stderr_handler.emit.assert_not_called()
    
    def test_emit_warning_to_stderr(self):
        record = logging.LogRecord(
            'test', logging.WARNING, 'test.py', 1, 'Warning message', (), None
        )
        
        self.handler.emit(record)
        
        self.stderr_handler.emit.assert_called_once_with(record)
        self.stdout_handler.emit.assert_not_called()
    
    def test_emit_error_to_stderr(self):
        record = logging.LogRecord(
            'test', logging.ERROR, 'test.py', 1, 'Error message', (), None
        )
        
        self.handler.emit(record)
        
        self.stderr_handler.emit.assert_called_once_with(record)
        self.stdout_handler.emit.assert_not_called()
    
    def test_emit_critical_to_stderr(self):
        record = logging.LogRecord(
            'test', logging.CRITICAL, 'test.py', 1, 'Critical message', (), None
        )
        
        self.handler.emit(record)
        
        self.stderr_handler.emit.assert_called_once_with(record)
        self.stdout_handler.emit.assert_not_called()
    
    def test_set_formatter(self):
        formatter = ColoredFormatter()
        
        self.handler.setFormatter(formatter)
        
        self.stdout_handler.setFormatter.assert_called_once_with(formatter)
        self.stderr_handler.setFormatter.assert_called_once_with(formatter)
    
    def test_set_level(self):
        level = logging.DEBUG
        
        self.handler.setLevel(level)
        
        self.stdout_handler.setLevel.assert_called_once_with(level)
        self.stderr_handler.setLevel.assert_called_once_with(level)
    
    def test_emit_handle_error(self):
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 'Test message', (), None
        )
        
        self.stdout_handler.emit.side_effect = Exception("Handler failed")
        
        with patch.object(self.handler, 'handleError') as mock_handle_error:
            self.handler.emit(record)
            mock_handle_error.assert_called_once_with(record)


if __name__ == '__main__':
    unittest.main() 