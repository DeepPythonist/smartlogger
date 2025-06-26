# Integration tests 

import unittest
import logging
import sys
from io import StringIO
from unittest.mock import patch, Mock

import smartlogger
from smartlogger import ColoredStreamHandler, ColoredFormatter, configure_colors
from smartlogger.core.monkey_patch import patch_logging, unpatch_logging
from smartlogger.auto import activate, deactivate
from smartlogger.config.colors import ANSIColors


class TestBasicIntegration(unittest.TestCase):
    
    def setUp(self):
        self.stream = StringIO()
        self.logger = logging.getLogger('test_integration')
        self.logger.handlers.clear()
        self.logger.setLevel(logging.DEBUG)
    
    def tearDown(self):
        self.logger.handlers.clear()
        try:
            unpatch_logging()
        except Exception:
            pass
    
    def test_colored_handler_with_logger(self):
        handler = ColoredStreamHandler(self.stream)
        self.logger.addHandler(handler)
        
        self.logger.info('Test info message')
        self.logger.error('Test error message')
        
        output = self.stream.getvalue()
        self.assertIn('Test info message', output)
        self.assertIn('Test error message', output)
    
    def test_colored_formatter_integration(self):
        handler = ColoredStreamHandler(self.stream)
        formatter = ColoredFormatter('%(levelname)s: %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        
        self.logger.warning('Test warning')
        
        output = self.stream.getvalue()
        self.assertIn('WARNING: Test warning', output)
    
    def test_multiple_handlers_same_logger(self):
        stream1 = StringIO()
        stream2 = StringIO()
        
        handler1 = ColoredStreamHandler(stream1)
        handler2 = ColoredStreamHandler(stream2)
        
        self.logger.addHandler(handler1)
        self.logger.addHandler(handler2)
        
        self.logger.info('Dual output test')
        
        output1 = stream1.getvalue()
        output2 = stream2.getvalue()
        
        self.assertIn('Dual output test', output1)
        self.assertIn('Dual output test', output2)


class TestMonkeyPatchingIntegration(unittest.TestCase):
    
    def setUp(self):
        self.original_handlers = logging.root.handlers.copy()
        self.test_logger = logging.getLogger('monkey_patch_test')
        self.test_logger.handlers.clear()
    
    def tearDown(self):
        try:
            unpatch_logging()
        except Exception:
            pass
        
        logging.root.handlers.clear()
        logging.root.handlers.extend(self.original_handlers)
        self.test_logger.handlers.clear()
    
    @patch('smartlogger.utils.terminal.supports_colors')
    def test_patch_logging_integration(self, mock_supports_colors):
        mock_supports_colors.return_value = True
        
        success = patch_logging()
        self.assertTrue(success)
        
        stream = StringIO()
        handler = ColoredStreamHandler(stream)
        self.test_logger.addHandler(handler)
        
        self.test_logger.info('Patched logging test')
        
        output = stream.getvalue()
        self.assertIn('Patched logging test', output)
    
    def test_unpatch_logging_restores_original(self):
        original_basic_config = logging.basicConfig
        
        patch_logging()
        unpatch_logging()
        
        self.assertEqual(logging.basicConfig, original_basic_config)


class TestAutoActivationIntegration(unittest.TestCase):
    
    def setUp(self):
        self.original_handlers = logging.root.handlers.copy()
    
    def tearDown(self):
        try:
            deactivate()
        except Exception:
            pass
        
        logging.root.handlers.clear()
        logging.root.handlers.extend(self.original_handlers)
    
    @patch('smartlogger.utils.terminal.supports_colors')
    def test_auto_activation(self, mock_supports_colors):
        mock_supports_colors.return_value = True
        
        success = activate()
        self.assertTrue(success)
        
        stream = StringIO()
        handler = ColoredStreamHandler(stream)
        logger = logging.getLogger('auto_test')
        logger.addHandler(handler)
        
        logger.debug('Auto activation test')
        
        output = stream.getvalue()
        self.assertIn('Auto activation test', output)


class TestColorConfigurationIntegration(unittest.TestCase):
    
    def setUp(self):
        self.stream = StringIO()
        self.handler = ColoredStreamHandler(self.stream, force_color=True)
        self.logger = logging.getLogger('color_config_test')
        self.logger.handlers.clear()
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)
    
    def tearDown(self):
        self.logger.handlers.clear()
    
    def test_configure_colors_integration(self):
        custom_colors = {
            'INFO': ANSIColors.BLUE,
            'WARNING': ANSIColors.MAGENTA
        }
        
        configure_colors(custom_colors)
        
        self.logger.info('Blue info message')
        self.logger.warning('Magenta warning message')
        
        output = self.stream.getvalue()
        self.assertIn('Blue info message', output)
        self.assertIn('Magenta warning message', output)
    
    def test_runtime_color_scheme_change(self):
        from smartlogger.config.colors import ColorScheme
        
        new_scheme = ColorScheme({
            'ERROR': ANSIColors.CYAN
        })
        
        self.handler.set_color_scheme(new_scheme)
        
        self.logger.error('Cyan error message')
        
        output = self.stream.getvalue()
        self.assertIn('Cyan error message', output)


class TestFullWorkflowIntegration(unittest.TestCase):
    
    def setUp(self):
        self.original_handlers = logging.root.handlers.copy()
    
    def tearDown(self):
        try:
            deactivate()
            unpatch_logging()
        except Exception:
            pass
        
        logging.root.handlers.clear()
        logging.root.handlers.extend(self.original_handlers)
    
    @patch('smartlogger.utils.terminal.supports_colors')
    def test_complete_workflow(self, mock_supports_colors):
        mock_supports_colors.return_value = True
        
        # Step 1: Auto activation
        activate()
        
        # Step 2: Configure custom colors
        configure_colors({
            'DEBUG': ANSIColors.CYAN,
            'INFO': ANSIColors.GREEN,
            'WARNING': ANSIColors.YELLOW,
            'ERROR': ANSIColors.RED,
            'CRITICAL': ANSIColors.BOLD + ANSIColors.RED
        })
        
        # Step 3: Create logger and test all levels
        stream = StringIO()
        handler = ColoredStreamHandler(stream, force_color=True)
        logger = logging.getLogger('workflow_test')
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)
        
        logger.debug('Debug message')
        logger.info('Info message')
        logger.warning('Warning message')
        logger.error('Error message')
        logger.critical('Critical message')
        
        output = stream.getvalue()
        
        # Verify all messages are present
        self.assertIn('Debug message', output)
        self.assertIn('Info message', output)
        self.assertIn('Warning message', output)
        self.assertIn('Error message', output)
        self.assertIn('Critical message', output)
        
        # Verify colors are applied
        self.assertIn(ANSIColors.CYAN, output)  # Debug
        self.assertIn(ANSIColors.GREEN, output)  # Info
        self.assertIn(ANSIColors.YELLOW, output)  # Warning
        self.assertIn(ANSIColors.RED, output)  # Error/Critical
        
        logger.handlers.clear()


class TestErrorHandlingIntegration(unittest.TestCase):
    
    def test_graceful_degradation_no_color_support(self):
        with patch('smartlogger.utils.terminal.supports_colors') as mock_supports:
            mock_supports.return_value = False
            
            stream = StringIO()
            handler = ColoredStreamHandler(stream)
            logger = logging.getLogger('no_color_test')
            logger.addHandler(handler)
            
            logger.info('No color test message')
            
            output = stream.getvalue()
            self.assertIn('No color test message', output)
            self.assertNotIn(ANSIColors.GREEN, output)
            
            logger.handlers.clear()
    
    def test_exception_handling_in_formatter(self):
        stream = StringIO()
        handler = ColoredStreamHandler(stream)
        
        # Create a record that might cause issues
        record = logging.LogRecord(
            'test', logging.INFO, 'test.py', 1, 
            'Test with %s formatting', ('arg',), None
        )
        
        # This should not raise an exception
        try:
            handler.emit(record)
            output = stream.getvalue()
            self.assertIn('Test with arg formatting', output)
        except Exception as e:
            self.fail(f"Handler should handle errors gracefully: {e}")


if __name__ == '__main__':
    unittest.main() 