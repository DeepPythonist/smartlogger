#!/bin/bash

# SmartLogger PyPI Upload Script
# Usage: ./upload_to_pypi.sh [test|prod]

set -e

echo "🚀 SmartLogger PyPI Upload Script"
echo "================================="

# Check if argument is provided
if [ -z "$1" ]; then
    echo "Usage: $0 [test|prod]"
    echo "  test - Upload to TestPyPI"
    echo "  prod - Upload to PyPI"
    exit 1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build/ dist/ *.egg-info/

# Build the package
echo "📦 Building package..."
python -m build

# Check the package
echo "🔍 Checking package integrity..."
python -m twine check dist/*

if [ "$1" = "test" ]; then
    echo "📤 Uploading to TestPyPI..."
    echo "Note: You'll need TestPyPI credentials"
    python -m twine upload --repository testpypi dist/*
    echo "✅ Package uploaded to TestPyPI!"
    echo "Install with: pip install --index-url https://test.pypi.org/simple/ pysmartlogger"
    
elif [ "$1" = "prod" ]; then
    echo "⚠️  WARNING: This will upload to PRODUCTION PyPI!"
    read -p "Are you sure you want to continue? (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "📤 Uploading to PyPI..."
        python -m twine upload dist/*
        echo "✅ Package uploaded to PyPI!"
        echo "Install with: pip install pysmartlogger"
    else
        echo "❌ Upload cancelled."
        exit 1
    fi
else
    echo "❌ Invalid argument. Use 'test' or 'prod'"
    exit 1
fi

echo "🎉 Done!" 