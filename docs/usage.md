# Usage Guide

## Basic Usage

The simplest way to use SmartLogger is to import the auto module:

```python
import logging
import smartlogger.auto

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("This appears in blue")
logger.info("This appears in green")
logger.warning("This appears in yellow")
logger.error("This appears in red")
logger.critical("This appears in bright red")
```

## Advanced Usage

### Using ColorFormatter Directly

```python
import logging
from smartlogger.core.formatter import ColorFormatter

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = ColorFormatter('%(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info("Custom formatted message")
```

### Using ColorHandler

```python
import logging
from smartlogger.core.handler import ColorHandler

logger = logging.getLogger(__name__)
handler = ColorHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.warning("Message with color handler")
```

### Manual Color Control

```python
from smartlogger.core.formatter import ColorFormatter

formatter = ColorFormatter()
formatter.disable_colors()  # Disable colors
formatter.enable_colors()   # Enable colors
```

## Integration with Existing Applications

SmartLogger works seamlessly with existing Python applications:

```python
import logging
import smartlogger.auto  # This line adds colors to all existing loggers

# Your existing logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)

# All your existing loggers now have colored output
logger = logging.getLogger('myapp')
logger.info("This will be colored in the console")
```

## Environment Detection

SmartLogger automatically detects your environment:

- **Terminal Support**: Checks for ANSI color capability
- **IDE Integration**: Works with VS Code, PyCharm, Jupyter notebooks
- **Cross-Platform**: Windows, macOS, and Linux support
- **Safe Fallback**: Plain text when colors aren't supported

## Color Scheme

| Log Level | Color | ANSI Code |
|-----------|-------|-----------|
| DEBUG | Blue | `\033[34m` |
| INFO | Green | `\033[32m` |
| WARNING | Yellow | `\033[33m` |
| ERROR | Red | `\033[31m` |
| CRITICAL | Bright Red + Bold | `\033[91m\033[1m` |

## Best Practices

1. **Import Early**: Import `smartlogger.auto` as early as possible in your application
2. **File Logging**: Colors are automatically disabled for file outputs
3. **Performance**: Minimal overhead - color detection is cached
4. **Compatibility**: Safe to use in production environments

## Common Patterns

### Web Application

```python
import logging
import smartlogger.auto

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app_logger = logging.getLogger('app')
db_logger = logging.getLogger('database')
api_logger = logging.getLogger('api')

app_logger.info("Application started")
db_logger.warning("Connection pool low")
api_logger.error("Request failed")
```

### Library Development

```python
import logging
import smartlogger.auto

class MyLibrary:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def process_data(self):
        self.logger.debug("Processing started")
        self.logger.info("Data processed successfully")
```