# Custom exceptions for SmartLogger 

class SmartLoggerError(Exception):
    pass


class ConfigurationError(SmartLoggerError):
    pass


class ColorFormatError(SmartLoggerError):
    pass


class TerminalDetectionError(SmartLoggerError):
    pass


class HandlerCreationError(SmartLoggerError):
    pass


class FormatterError(SmartLoggerError):
    pass


class PatchingError(SmartLoggerError):
    pass


class UnsupportedPlatformError(SmartLoggerError):
    pass 