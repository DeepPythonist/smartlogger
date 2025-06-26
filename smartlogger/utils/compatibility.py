import sys
import os
from .terminal import is_windows

_ansi_enabled = False

def enable_windows_ansi_support():
    global _ansi_enabled
    
    if _ansi_enabled or not is_windows():
        return True
    
    try:
        import ctypes
        from ctypes import wintypes
        
        kernel32 = ctypes.windll.kernel32
        
        STD_OUTPUT_HANDLE = -11
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004
        
        stdout_handle = kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
        if stdout_handle == -1:
            return False
        
        mode = wintypes.DWORD()
        if not kernel32.GetConsoleMode(stdout_handle, ctypes.byref(mode)):
            return False
        
        mode.value |= ENABLE_VIRTUAL_TERMINAL_PROCESSING
        if not kernel32.SetConsoleMode(stdout_handle, mode):
            return False
        
        _ansi_enabled = True
        return True
        
    except Exception:
        try:
            os.system('color')
            _ansi_enabled = True
            return True
        except:
            return False

def ensure_color_support():
    if is_windows():
        return enable_windows_ansi_support()
    return True 