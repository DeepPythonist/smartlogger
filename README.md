# SmartLogger

A cross-platform Python library that adds beautiful, colorful logging capabilities to the standard Python logging module with zero configuration required.

## Features

- 🎨 **Colorful Logs**: Each log level gets its distinctive color
- 🔧 **Zero Configuration**: Just import and it works automatically  
- 🖥️ **Cross-Platform**: Works on Windows, macOS, and Linux
- 🏃 **Performance Optimized**: Minimal overhead on your application
- 🛡️ **Safe**: Won't break existing logging functionality
- 📱 **Smart Detection**: Automatically detects terminal capabilities

## Installation

```bash
pip install pysmartlogger
```

## Usage

Simply import `smartlogger.auto` and your existing logging will become colorful:

```python
import logging
import smartlogger.auto

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

logger.debug("This is a debug message")     # Blue
logger.info("This is an info message")      # Green  
logger.warning("This is a warning message") # Yellow
logger.error("This is an error message")    # Red
logger.critical("This is a critical message") # Bright Red
```

## Color Scheme

| Level | Color | Description |
|-------|-------|-------------|
| DEBUG | Blue | Development and debugging information |
| INFO | Green | General information messages |
| WARNING | Yellow | Warning messages for potential issues |
| ERROR | Red | Error messages for failures |
| CRITICAL | Bright Red | Critical errors requiring immediate attention |

## Compatibility

- **Python**: 3.7+
- **Operating Systems**: Windows, macOS, Linux
- **Terminals**: CMD, PowerShell, bash, zsh, fish
- **IDEs**: VS Code, PyCharm, Jupyter, and more

## How It Works

SmartLogger uses monkey-patching to enhance the standard logging module. When you import `smartlogger.auto`, it automatically:

1. Detects if your environment supports colors
2. Patches the logging formatters to add color codes
3. Maintains full compatibility with existing logging configuration

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Author

**Mohammad Rasol Esfandiari**  
- GitHub: [@DeepPythonist](https://github.com/DeepPythonist)
- Email: mrasolesfandiari@gmail.com 