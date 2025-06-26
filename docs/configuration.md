# Configuration Guide

## Environment Variables

SmartLogger respects several environment variables for color control:

### Color Control Variables

- `NO_COLOR`: Disable all colors when set (any value)
- `FORCE_COLOR`: Force colors even in non-TTY environments
- `COLORTERM`: Indicates terminal color support (`truecolor`, `24bit`)
- `TERM`: Terminal type detection (`xterm-256color`, `screen-256color`, etc.)

### Examples

```bash
# Disable colors
export NO_COLOR=1
python your_app.py

# Force colors
export FORCE_COLOR=1
python your_app.py

# Set terminal type
export TERM=xterm-256color
python your_app.py
```

## Programmatic Configuration

### Disable Colors Globally

```python
import logging
import smartlogger.auto
from smartlogger.core.monkey_patch import unpatch_logging

# Disable SmartLogger
unpatch_logging()

# Or check if already patched
from smartlogger.core.monkey_patch import is_patched
if is_patched():
    print("SmartLogger is active")
```

### Custom Color Scheme

```python
from smartlogger.config.colors import Colors

# Modify default colors
Colors.DEBUG = Colors.CYAN
Colors.INFO = Colors.BLUE
Colors.WARNING = Colors.MAGENTA
```

### Custom Formatter

```python
import logging
from smartlogger.core.formatter import ColorFormatter

class CustomColorFormatter(ColorFormatter):
    def format(self, record):
        # Add custom formatting logic
        formatted = super().format(record)
        return f"[CUSTOM] {formatted}"

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(CustomColorFormatter())
logger.addHandler(handler)
```

## Platform-Specific Configuration

### Windows Configuration

SmartLogger automatically enables ANSI support on Windows:

```python
from smartlogger.utils.compatibility import enable_windows_ansi_support

# This is called automatically, but you can call it manually
if enable_windows_ansi_support():
    print("ANSI colors enabled on Windows")
```

### IDE Configuration

For specific IDE support:

```python
from smartlogger.utils.terminal import is_ide_environment

if is_ide_environment():
    print("Running in IDE environment")
```

## Logging Configuration Integration

### Using with dictConfig

```python
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'colored': {
            '()': 'smartlogger.core.formatter.ColorFormatter',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'smartlogger.core.handler.ColorHandler',
            'formatter': 'colored'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    }
}

logging.config.dictConfig(LOGGING_CONFIG)
```

### Using with fileConfig

Create a file `logging.conf`:

```ini
[loggers]
keys=root

[handlers]
keys=console

[formatters]
keys=colored

[logger_root]
level=INFO
handlers=console

[handler_console]
class=smartlogger.core.handler.ColorHandler
formatter=colored

[formatter_colored]
class=smartlogger.core.formatter.ColorFormatter
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```

Then use it:

```python
import logging.config
logging.config.fileConfig('logging.conf')
```

## Performance Configuration

### Disable Color Detection

```python
from smartlogger.core.formatter import ColorFormatter

# Create formatter with colors disabled
formatter = ColorFormatter()
formatter.disable_colors()
```

### Cache Control

Color detection is automatically cached, but you can control it:

```python
from smartlogger.utils.terminal import is_terminal_supports_color

# This result is cached after first call
supports_color = is_terminal_supports_color()
```

## Development vs Production

### Development

```python
import logging
import smartlogger.auto

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Production

```python
import logging
import os

# Only enable colors in development
if os.getenv('ENVIRONMENT') == 'development':
    import smartlogger.auto

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
``` 