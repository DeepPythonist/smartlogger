# Installation Guide

## Requirements

- Python 3.7 or higher
- No external dependencies required

## Installation Methods

### Option 1: From Source (Current)

1. Clone or download the SmartLogger project
2. Navigate to the project directory
3. Install in development mode:

```bash
pip install -e .
```

### Option 2: Using pip (Future)

```bash
pip install smartlogger
```

### Option 3: Using conda (Future)

```bash
conda install -c conda-forge smartlogger
```

## Verification

Test your installation:

```python
import smartlogger
print(smartlogger.get_version())
```

Or run a simple test:

```python
import smartlogger.auto
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('test')
logger.info('SmartLogger is working!')
```

## Platform Support

SmartLogger supports:

- **Linux**: Full support with ANSI colors
- **macOS**: Full support with ANSI colors  
- **Windows**: Full support on Windows 10+ with ANSI support
- **Older Windows**: Graceful degradation to plain text

## Terminal Support

SmartLogger automatically detects terminal capabilities:

- **Color Support**: Automatically detected
- **Interactive vs Non-interactive**: Handled appropriately
- **Environment Variables**: 
  - `NO_COLOR`: Disables colors
  - `FORCE_COLOR`: Forces colors even in non-interactive mode

## Troubleshooting

### Colors not appearing
- Check if your terminal supports ANSI colors
- Verify `NO_COLOR` environment variable is not set
- Try setting `FORCE_COLOR=1` environment variable

### Import errors
- Ensure Python 3.7+ is being used
- Verify installation completed successfully
- Check for conflicting packages

### Performance issues
- SmartLogger has minimal overhead
- If issues persist, disable auto-discovery and use manual configuration 