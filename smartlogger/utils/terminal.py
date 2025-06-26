import os
import sys
import platform

def is_windows():
    return platform.system().lower() == 'windows'

def is_colorama_available():
    try:
        import colorama
        return True
    except ImportError:
        return False

def is_tty():
    return hasattr(sys.stdout, 'isatty') and sys.stdout.isatty()

def has_color_env_var():
    term = os.environ.get('TERM', '')
    colorterm = os.environ.get('COLORTERM', '')
    force_color = os.environ.get('FORCE_COLOR', '')
    no_color = os.environ.get('NO_COLOR', '')
    
    if no_color:
        return False
    if force_color:
        return True
    if colorterm in ('truecolor', '24bit'):
        return True
    if term in ('xterm-256color', 'screen-256color', 'xterm-color', 'cygwin'):
        return True
    return False

def is_ide_environment():
    ide_indicators = [
        'PYCHARM_HOSTED',
        'VSCODE_PID',
        'TERM_PROGRAM',
        'JPY_PARENT_PID',
        'COLAB_GPU'
    ]
    
    for indicator in ide_indicators:
        if os.environ.get(indicator):
            return True
    
    if hasattr(sys, 'ps1'):
        return True
    
    return False

def is_windows_terminal():
    if not is_windows():
        return False
    
    wt_session = os.environ.get('WT_SESSION')
    if wt_session:
        return True
    
    term_program = os.environ.get('TERM_PROGRAM', '')
    if 'WindowsTerminal' in term_program:
        return True
    
    return False

def is_powershell():
    return 'powershell' in os.environ.get('PSModulePath', '').lower()

def is_cmd():
    if not is_windows():
        return False
    return os.environ.get('PROMPT') is not None

def supports_ansi_colors():
    if is_windows():
        if is_windows_terminal() or is_powershell():
            return True
        
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            stdout_handle = kernel32.GetStdHandle(-11)
            mode = ctypes.c_ulong()
            kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode))
            return bool(mode.value & 0x0004)
        except:
            return False
    
    return True

def is_terminal_supports_color():
    if not is_tty() and not is_ide_environment():
        return False
    
    if has_color_env_var():
        return True
    
    if is_ide_environment():
        return True
    
    if supports_ansi_colors():
        return True
    
    return False 