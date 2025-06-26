# Installation Guide

## Requirements

- Python 3.8 or higher
- No external dependencies required

## Installation from PyPI

```bash
pip install pysmartlogger
```

## Installation from Source

### Clone the Repository

```bash
git clone https://github.com/DeepPythonist/smartlogger.git
cd smartlogger
```

### Install in Development Mode

```bash
pip install -e .
```

### Install for Production

```bash
pip install .
```

## Verification

To verify the installation works correctly:

```python
import logging
import smartlogger.auto

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test')

logger.info("SmartLogger is working!")
```

You should see the message displayed in green color (if your terminal supports colors).

## Troubleshooting

### Colors Not Showing

If colors are not displaying:

1. Check if your terminal supports ANSI colors
2. Verify environment variables: `TERM`, `COLORTERM`
3. For Windows: Use Windows Terminal or PowerShell
4. For IDEs: Most modern IDEs support colored output

### ImportError

If you get import errors:

1. Ensure Python version is 3.8+
2. Verify installation with `pip list | grep smartlogger`
3. Check if you're using the correct Python environment

## Uninstallation

```bash
pip uninstall pysmartlogger
``` 