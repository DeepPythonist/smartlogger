import unittest
import sys
import logging
from unittest.mock import patch, MagicMock

class TestAutoModule(unittest.TestCase):
    
    def setUp(self):
        if 'smartlogger.auto' in sys.modules:
            del sys.modules['smartlogger.auto']
        if 'smartlogger.core.monkey_patch' in sys.modules:
            del sys.modules['smartlogger.core.monkey_patch']
    
    def test_auto_import_with_existing_logging(self):
        with patch('smartlogger.core.monkey_patch.patch_logging') as mock_patch:
            import smartlogger.auto
            mock_patch.assert_called_once()
    
    def test_auto_import_safe_on_exception(self):
        with patch('smartlogger.core.monkey_patch.patch_logging', side_effect=Exception("Test error")):
            try:
                import smartlogger.auto
            except Exception:
                self.fail("Auto import should not raise exceptions")
    
    def test_logging_functionality_after_import(self):
        import smartlogger.auto
        
        logger = logging.getLogger('test')
        
        with patch.object(logger, 'debug') as mock_debug:
            logger.debug("Test message")
            mock_debug.assert_called_once_with("Test message")

if __name__ == '__main__':
    unittest.main() 