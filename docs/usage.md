# Usage Guide

## Quick Start

The simplest way to use SmartLogger:

```python
import smartlogger.auto
import logging

# Your existing logging code now has colors!
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("Debug message")
logger.info("Info message") 
logger.warning("Warning message")
logger.error("Error message")
logger.critical("Critical message")
```

## Manual Configuration

For more control, use manual configuration:

```python
import logging
from smartlogger import ColoredStreamHandler, ColoredFormatter

# Create colored handler
handler = ColoredStreamHandler()
formatter = ColoredFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Configure logger
logger = logging.getLogger('myapp')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
```

## Formatter Options

### Basic Colored Formatter
```python
from smartlogger import ColoredFormatter

formatter = ColoredFormatter()
```

### Minimal Formatter
```python
from smartlogger import MinimalColoredFormatter

formatter = MinimalColoredFormatter()  # Just "LEVEL: message"
```

### Detailed Formatter
```python
from smartlogger import DetailedColoredFormatter

formatter = DetailedColoredFormatter()  # Includes timestamp and logger name
```

### JSON Formatter
```python
from smartlogger import JSONColoredFormatter

formatter = JSONColoredFormatter()  # Colored JSON output
```

## Handler Options

### Console Handler
```python
from smartlogger import ColoredConsoleHandler

# Stderr (default)
handler = ColoredConsoleHandler()

# Stdout
handler = ColoredConsoleHandler(use_stderr=False)
```

### File Handler
```python
from smartlogger import ColoredFileHandler

# Plain file (colors disabled by default)
handler = ColoredFileHandler('app.log')

# Colored file output
handler = ColoredFileHandler('app.log', force_color=True)
```

### Smart Handler with Fallback
```python
from smartlogger import SmartColorHandler
import logging

fallback = logging.StreamHandler()
handler = SmartColorHandler(fallback_handler=fallback)
```

### Dual Output Handler
```python
from smartlogger import DualOutputHandler

handler = DualOutputHandler()  # INFO+ to stdout, WARNING+ to stderr
```

## Color Customization

### Custom Color Scheme
```python
import smartlogger
from smartlogger.config.colors import ANSIColors

smartlogger.configure_colors({
    'DEBUG': ANSIColors.CYAN,
    'INFO': ANSIColors.GREEN,
    'WARNING': ANSIColors.YELLOW,
    'ERROR': ANSIColors.RED,
    'CRITICAL': ANSIColors.BOLD + ANSIColors.RED + ANSIColors.BG_WHITE
})
```

### Runtime Color Changes
```python
from smartlogger.config.colors import ColorScheme

new_scheme = ColorScheme({
    'INFO': ANSIColors.BLUE,
    'ERROR': ANSIColors.MAGENTA
})

handler.set_color_scheme(new_scheme)
```

### Enable/Disable Colors
```python
# Globally
smartlogger.enable_colors()
smartlogger.disable_colors()

# Per handler
handler.enable_colors()
handler.disable_colors()

# Per formatter
formatter.enable_colors()
formatter.disable_colors()
```

## Advanced Usage

### Monkey Patching
```python
from smartlogger.core.monkey_patch import patch_logging, unpatch_logging

# Apply patches
patch_logging(
    patch_root=True,
    preserve_existing=True,
    add_colored_handler=True
)

# Remove patches
unpatch_logging()
```

### Multiple Loggers
```python
import logging
from smartlogger import ColoredStreamHandler

# App logger
app_logger = logging.getLogger('myapp')
app_handler = ColoredStreamHandler()
app_logger.addHandler(app_handler)

# Database logger with different colors
db_logger = logging.getLogger('myapp.db')
db_handler = ColoredStreamHandler()
db_handler.set_color_scheme(ColorScheme({
    'INFO': ANSIColors.CYAN,
    'ERROR': ANSIColors.MAGENTA
}))
db_logger.addHandler(db_handler)
```

### Integration with Existing Code
```python
# Before (existing code)
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# After (with SmartLogger)
import smartlogger.auto  # Add this line
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

## Best Practices

1. **Import auto early**: Import `smartlogger.auto` before other logging configuration
2. **Use appropriate formatters**: Minimal for development, Detailed for production
3. **Respect NO_COLOR**: SmartLogger automatically handles this environment variable
4. **Test color support**: Verify colors work in your deployment environment
5. **File logging**: Disable colors for file outputs unless specifically needed
6. **Performance**: SmartLogger adds minimal overhead, but test in high-volume scenarios 