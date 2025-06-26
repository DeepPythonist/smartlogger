# Monkey patching functionality for logging module 

import logging
import sys
import threading
from typing import Dict, List, Optional, Any, Set

from ..config.colors import get_default_scheme
from ..utils.compatibility import (
    get_root_logger,
    get_logging_handlers,
    add_handler_to_logger,
    safe_getattr
)
from ..exceptions import PatchingError
from .handler import ColoredStreamHandler
from .formatter import ColoredFormatter


class LoggingPatcher:
    _instance = None
    _lock = threading.Lock()
    _patched = False
    _original_handlers = {}
    _added_handlers = []
    
    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._patched_loggers = set()
            self._backup_handlers = {}
    
    def patch_logging(
        self, 
        patch_root: bool = True,
        preserve_existing: bool = True,
        add_colored_handler: bool = True
    ) -> bool:
        try:
            with self._lock:
                if self._patched:
                    return True
                
                if patch_root:
                    self._patch_root_logger(preserve_existing, add_colored_handler)
                
                self._patch_logger_class()
                self._patch_basic_config()
                
                self._patched = True
                return True
                
        except Exception as e:
            raise PatchingError(f"Failed to patch logging: {e}")
    
    def unpatch_logging(self) -> bool:
        try:
            with self._lock:
                if not self._patched:
                    return True
                
                self._restore_original_handlers()
                self._restore_logger_class()
                self._restore_basic_config()
                
                self._patched = False
                return True
                
        except Exception as e:
            raise PatchingError(f"Failed to unpatch logging: {e}")
    
    def _patch_root_logger(self, preserve_existing: bool, add_colored_handler: bool):
        root_logger = get_root_logger()
        
        if preserve_existing:
            self._backup_handlers[root_logger] = get_logging_handlers(root_logger)
        
        if add_colored_handler:
            colored_handler = ColoredStreamHandler()
            colored_handler.setFormatter(ColoredFormatter())
            
            existing_handlers = get_logging_handlers(root_logger)
            has_stream_handler = any(
                isinstance(h, logging.StreamHandler) for h in existing_handlers
            )
            
            if not has_stream_handler or not preserve_existing:
                add_handler_to_logger(root_logger, colored_handler)
                self._added_handlers.append((root_logger, colored_handler))
    
    def _patch_logger_class(self):
        if not hasattr(logging.Logger, '_original_addHandler'):
            logging.Logger._original_addHandler = logging.Logger.addHandler
            
            def enhanced_add_handler(logger_self, handler):
                return self._enhanced_add_handler(logger_self, handler)
            
            logging.Logger.addHandler = enhanced_add_handler
    
    def _patch_basic_config(self):
        if not hasattr(logging, '_original_basicConfig'):
            logging._original_basicConfig = logging.basicConfig
            logging.basicConfig = self._enhanced_basic_config
    
    def _enhanced_add_handler(self, logger_self, handler):
        if isinstance(handler, logging.StreamHandler) and not isinstance(handler, ColoredStreamHandler):
            if hasattr(handler, 'stream') and hasattr(handler.stream, 'isatty'):
                try:
                    if handler.stream.isatty():
                        colored_handler = ColoredStreamHandler(
                            stream=handler.stream,
                            color_scheme=get_default_scheme()
                        )
                        if handler.formatter:
                            colored_formatter = ColoredFormatter()
                            colored_formatter._fmt = handler.formatter._fmt
                            colored_handler.setFormatter(colored_formatter)
                        
                        logger_self._original_addHandler(colored_handler)
                        return
                except Exception:
                    pass
        
        logger_self._original_addHandler(handler)
    
    def _enhanced_basic_config(self, **kwargs):
        if 'handlers' not in kwargs and 'stream' not in kwargs:
            kwargs['handlers'] = [ColoredStreamHandler()]
        
        return logging._original_basicConfig(**kwargs)
    
    def _restore_original_handlers(self):
        for logger, handlers in self._backup_handlers.items():
            logger.handlers.clear()
            for handler in handlers:
                logger.addHandler(handler)
        
        for logger, handler in self._added_handlers:
            try:
                logger.removeHandler(handler)
            except (ValueError, AttributeError):
                pass
        
        self._backup_handlers.clear()
        self._added_handlers.clear()
    
    def _restore_logger_class(self):
        if hasattr(logging.Logger, '_original_addHandler'):
            logging.Logger.addHandler = logging.Logger._original_addHandler
            delattr(logging.Logger, '_original_addHandler')
    
    def _restore_basic_config(self):
        if hasattr(logging, '_original_basicConfig'):
            logging.basicConfig = logging._original_basicConfig
            delattr(logging, '_original_basicConfig')
    
    def patch_logger(self, logger: logging.Logger, force: bool = False) -> bool:
        try:
            if logger in self._patched_loggers and not force:
                return True
            
            existing_handlers = get_logging_handlers(logger)
            stream_handlers = [
                h for h in existing_handlers 
                if isinstance(h, logging.StreamHandler) and not isinstance(h, ColoredStreamHandler)
            ]
            
            for handler in stream_handlers:
                if hasattr(handler, 'stream') and hasattr(handler.stream, 'isatty'):
                    try:
                        if handler.stream.isatty():
                            colored_handler = ColoredStreamHandler(
                                stream=handler.stream,
                                color_scheme=get_default_scheme()
                            )
                            
                            if handler.formatter:
                                colored_formatter = ColoredFormatter()
                                if hasattr(handler.formatter, '_fmt'):
                                    colored_formatter._fmt = handler.formatter._fmt
                                colored_handler.setFormatter(colored_formatter)
                            
                            logger.removeHandler(handler)
                            logger.addHandler(colored_handler)
                            
                            self._added_handlers.append((logger, colored_handler))
                    except Exception:
                        continue
            
            self._patched_loggers.add(logger)
            return True
            
        except Exception as e:
            return False
    
    @property
    def is_patched(self) -> bool:
        return self._patched
    
    @property
    def patched_loggers(self) -> Set[logging.Logger]:
        return self._patched_loggers.copy()


_patcher = LoggingPatcher()


def patch_logging(
    patch_root: bool = True,
    preserve_existing: bool = True,
    add_colored_handler: bool = True
) -> bool:
    return _patcher.patch_logging(patch_root, preserve_existing, add_colored_handler)


def unpatch_logging() -> bool:
    return _patcher.unpatch_logging()


def patch_logger(logger: logging.Logger, force: bool = False) -> bool:
    return _patcher.patch_logger(logger, force)


def is_patched() -> bool:
    return _patcher.is_patched


def get_patched_loggers() -> Set[logging.Logger]:
    return _patcher.patched_loggers 