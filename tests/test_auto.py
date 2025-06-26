# Tests for auto-discovery functionality 

import unittest
import logging
import sys
from unittest.mock import patch, MagicMock

import smartlogger.auto
from smartlogger.auto import AutoConfigurator, activate, deactivate, is_active, configure_colors
from smartlogger.core.monkey_patch import is_patched
from smartlogger.exceptions import SmartLoggerError


class TestAutoConfigurator(unittest.TestCase):
    
    def setUp(self):
        self.original_supports_colors = smartlogger.auto.supports_colors
        if hasattr(AutoConfigurator, '_instance'):
            AutoConfigurator._instance = None
        AutoConfigurator._activated = False
    
    def tearDown(self):
        smartlogger.auto.supports_colors = self.original_supports_colors
        try:
            deactivate()
        except Exception:
            pass
        if hasattr(AutoConfigurator, '_instance'):
            AutoConfigurator._instance = None
        AutoConfigurator._activated = False
    
    def test_singleton_pattern(self):
        configurator1 = AutoConfigurator()
        configurator2 = AutoConfigurator()
        self.assertIs(configurator1, configurator2)
    
    @patch('smartlogger.auto.supports_colors')
    @patch('smartlogger.auto.patch_logging')
    def test_activate_success(self, mock_patch, mock_supports):
        mock_supports.return_value = True
        mock_patch.return_value = True
        
        configurator = AutoConfigurator()
        result = configurator.activate()
        
        self.assertTrue(result)
        self.assertTrue(configurator._activated)
        mock_patch.assert_called_once()
    
    @patch('smartlogger.auto.supports_colors')
    def test_activate_no_color_support(self, mock_supports):
        mock_supports.return_value = False
        
        configurator = AutoConfigurator()
        result = configurator.activate()
        
        self.assertFalse(result)
        self.assertFalse(configurator._activated)
    
    @patch('smartlogger.auto.supports_colors')
    @patch('smartlogger.auto.patch_logging')
    def test_activate_patch_failure(self, mock_patch, mock_supports):
        mock_supports.return_value = True
        mock_patch.return_value = False
        
        configurator = AutoConfigurator()
        result = configurator.activate()
        
        self.assertFalse(result)
        self.assertFalse(configurator._activated)
    
    @patch('smartlogger.auto.unpatch_logging')
    def test_deactivate_success(self, mock_unpatch):
        mock_unpatch.return_value = True
        
        configurator = AutoConfigurator()
        configurator._activated = True
        result = configurator.deactivate()
        
        self.assertTrue(result)
        self.assertFalse(configurator._activated)
        mock_unpatch.assert_called_once()
    
    def test_deactivate_already_inactive(self):
        configurator = AutoConfigurator()
        configurator._activated = False
        result = configurator.deactivate()
        
        self.assertTrue(result)
        self.assertFalse(configurator._activated)
    
    @patch('smartlogger.auto.is_patched')
    def test_is_active(self, mock_is_patched):
        mock_is_patched.return_value = True
        
        configurator = AutoConfigurator()
        configurator._activated = True
        
        self.assertTrue(configurator.is_active())
        mock_is_patched.assert_called_once()
    
    @patch('smartlogger.auto.configure_colors')
    def test_configure_colors_success(self, mock_configure):
        mock_configure.return_value = None
        
        configurator = AutoConfigurator()
        colors = {'INFO': 'blue'}
        result = configurator.configure_colors(colors)
        
        self.assertTrue(result)
        mock_configure.assert_called_once_with(colors)
    
    @patch('smartlogger.auto.configure_colors')
    def test_configure_colors_failure(self, mock_configure):
        mock_configure.side_effect = Exception("Configuration failed")
        
        configurator = AutoConfigurator()
        colors = {'INFO': 'blue'}
        result = configurator.configure_colors(colors)
        
        self.assertFalse(result)


class TestPublicAPI(unittest.TestCase):
    
    def setUp(self):
        if hasattr(AutoConfigurator, '_instance'):
            AutoConfigurator._instance = None
        AutoConfigurator._activated = False
    
    def tearDown(self):
        try:
            deactivate()
        except Exception:
            pass
        if hasattr(AutoConfigurator, '_instance'):
            AutoConfigurator._instance = None
        AutoConfigurator._activated = False
    
    @patch('smartlogger.auto.supports_colors')
    @patch('smartlogger.auto.patch_logging')
    def test_activate_function(self, mock_patch, mock_supports):
        mock_supports.return_value = True
        mock_patch.return_value = True
        
        result = activate()
        self.assertTrue(result)
    
    @patch('smartlogger.auto.unpatch_logging')
    def test_deactivate_function(self, mock_unpatch):
        mock_unpatch.return_value = True
        
        result = deactivate()
        self.assertTrue(result)
    
    @patch('smartlogger.auto.is_patched')
    def test_is_active_function(self, mock_is_patched):
        mock_is_patched.return_value = True
        AutoConfigurator._activated = True
        
        result = is_active()
        self.assertTrue(result)
    
    def test_configure_colors_function(self):
        colors = {'DEBUG': 'cyan'}
        result = configure_colors(colors)
        self.assertIsInstance(result, bool)


class TestAutoImport(unittest.TestCase):
    
    def test_auto_configurator_creation(self):
        with patch('smartlogger.auto.AutoConfigurator') as mock_class:
            mock_instance = MagicMock()
            mock_class.return_value = mock_instance
            
            import importlib
            importlib.reload(smartlogger.auto)
            
            mock_class.assert_called()


if __name__ == '__main__':
    unittest.main() 