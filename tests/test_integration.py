import unittest
import logging
import sys
from io import StringIO
from unittest.mock import patch
import smartlogger.auto
from smartlogger.core.monkey_patch import is_patched, unpatch_logging

class TestIntegration(unittest.TestCase):
    
    def setUp(self):
        self.stream = StringIO()
        self.handler = logging.StreamHandler(self.stream)
        self.logger = logging.getLogger('test_integration')
        self.logger.addHandler(self.handler)
        self.logger.setLevel(logging.DEBUG)
        unpatch_logging()
    
    def tearDown(self):
        self.logger.removeHandler(self.handler)
        unpatch_logging()
    
    def test_logging_patched_after_auto_import(self):
        import smartlogger.auto
        logger = logging.getLogger('patch_test')
        logger.info("This should work whether patched or not")
        self.assertTrue(True)
    
    @patch('smartlogger.utils.terminal.is_terminal_supports_color', return_value=True)
    def test_colored_output_in_terminal(self, mock_supports_color):
        self.logger.info("Test message")
        output = self.stream.getvalue()
        self.assertIn('Test message', output)
    
    @patch('smartlogger.utils.terminal.is_terminal_supports_color', return_value=False)
    def test_plain_output_without_terminal_support(self, mock_supports_color):
        self.logger.info("Test message")
        output = self.stream.getvalue()
        self.assertIn('Test message', output)
    
    def test_all_log_levels_work(self):
        levels = [
            (logging.DEBUG, "Debug message"),
            (logging.INFO, "Info message"),
            (logging.WARNING, "Warning message"),
            (logging.ERROR, "Error message"),
            (logging.CRITICAL, "Critical message")
        ]
        
        for level, message in levels:
            with self.subTest(level=level):
                self.stream.seek(0)
                self.stream.truncate(0)
                self.logger.log(level, message)
                output = self.stream.getvalue()
                self.assertIn(message, output)
    
    def test_multiple_loggers_work_independently(self):
        logger1 = logging.getLogger('test1')
        logger2 = logging.getLogger('test2')
        
        stream1 = StringIO()
        stream2 = StringIO()
        
        handler1 = logging.StreamHandler(stream1)
        handler2 = logging.StreamHandler(stream2)
        
        logger1.addHandler(handler1)
        logger2.addHandler(handler2)
        
        logger1.setLevel(logging.INFO)
        logger2.setLevel(logging.DEBUG)
        
        logger1.info("Logger 1 message")
        logger2.debug("Logger 2 message")
        
        output1 = stream1.getvalue()
        output2 = stream2.getvalue()
        
        self.assertIn("Logger 1 message", output1)
        self.assertIn("Logger 2 message", output2)
        
        logger1.removeHandler(handler1)
        logger2.removeHandler(handler2)

if __name__ == '__main__':
    unittest.main() 