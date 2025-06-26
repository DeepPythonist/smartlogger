# Configuration Guide

## Auto-Discovery Configuration

SmartLogger can automatically activate when imported:

```python
import smartlogger.auto  # Automatic activation
```

### Auto-Discovery Control

```python
from smartlogger.auto import activate, deactivate, is_active

# Manual control
activate()    # Enable SmartLogger
deactivate()  # Disable SmartLogger
is_active()   # Check status
```

## Color Configuration

### Default Color Scheme

```python
{
    'DEBUG': 'Bright Blue',
    'INFO': 'Green', 
    'WARNING': 'Yellow',
    'ERROR': 'Red',
    'CRITICAL': 'Bold Red with White Background'
}
```

### Custom Colors

```python
import smartlogger
from smartlogger.config.colors import ANSIColors

# Method 1: Using configure_colors
smartlogger.configure_colors({
    'DEBUG': ANSIColors.CYAN,
    'INFO': ANSIColors.BRIGHT_GREEN,
    'WARNING': ANSIColors.MAGENTA,
    'ERROR': ANSIColors.BRIGHT_RED,
    'CRITICAL': ANSIColors.BOLD + ANSIColors.YELLOW
})

# Method 2: Using ColorScheme
from smartlogger.config.colors import ColorScheme
scheme = ColorScheme({
    'INFO': ANSIColors.BLUE,
    'ERROR': ANSIColors.RED
})
```

### Available Colors

#### Basic Colors
- `ANSIColors.BLACK`
- `ANSIColors.RED`
- `ANSIColors.GREEN`
- `ANSIColors.YELLOW`
- `ANSIColors.BLUE`
- `ANSIColors.MAGENTA`
- `ANSIColors.CYAN`
- `ANSIColors.WHITE`

#### Bright Colors
- `ANSIColors.BRIGHT_BLACK`
- `ANSIColors.BRIGHT_RED`
- `ANSIColors.BRIGHT_GREEN`
- `ANSIColors.BRIGHT_YELLOW`
- `ANSIColors.BRIGHT_BLUE`
- `ANSIColors.BRIGHT_MAGENTA`
- `ANSIColors.BRIGHT_CYAN`
- `ANSIColors.BRIGHT_WHITE`

## Environment Variables

### Color Control
- `NO_COLOR`: Disables all colors when set
- `FORCE_COLOR`: Forces colors even in non-interactive environments
- `TERM`: Used for terminal capability detection

### Usage Examples

```bash
# Disable colors
export NO_COLOR=1
python myapp.py

# Force colors
export FORCE_COLOR=1
python myapp.py

# Set terminal type
export TERM=xterm-256color
python myapp.py
``` 