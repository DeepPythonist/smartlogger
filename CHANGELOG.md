# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.0] - 2025-01-06

### Added
- Enhanced cross-platform compatibility
- Improved Windows ANSI support
- Better IDE environment detection
- More robust terminal color detection
- Performance optimizations

### Fixed
- Fixed color display issues in certain terminals
- Improved monkey patching reliability
- Better error handling for edge cases

### Changed
- Updated documentation with more examples
- Refined test coverage
- Improved code structure and organization

## [1.0.0] - 2024-01-06

### Added
- Initial release of SmartLogger
- Auto monkey-patching for Python logging module
- Cross-platform color support for terminal and console outputs
- Automatic terminal detection and color capability assessment
- Zero-dependency implementation
- Support for all standard logging levels with distinct colors
- Safe import mechanism that doesn't break existing logging functionality
- Performance-optimized color formatting

### Features
- DEBUG logs in blue
- INFO logs in green  
- WARNING logs in yellow
- ERROR logs in red
- CRITICAL logs in bright red
- Automatic fallback to plain text in non-color environments
- Windows CMD, PowerShell, and Unix terminal support
- IDE and editor compatibility 