# SmartLogger

A colorful logging extension for Python's built-in logging module.

## Features

- 🎨 Colorful log output
- 🔧 Easy integration with existing logging code
- ⚙️ Customizable color schemes
- 🚀 Zero-configuration auto-discovery
- 💻 Cross-platform terminal support

## Installation

```bash
pip install smartlogger
```

## Quick Start

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

## License

MIT License 