#!/bin/bash
# Installation script for Simple Editor

echo "Installing Simple Editor..."

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    echo "Please install pip3 or upgrade Python 3"
    exit 1
fi

# Install the package
echo "Installing Simple Editor via pip..."
pip3 install .

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Simple Editor installed successfully!"
    echo ""
    echo "You can now run it with:"
    echo "  simple-editor"
    echo "  or"
    echo "  simple-editor-gui"
    echo ""
    echo "Or run directly with:"
    echo "  python3 simple_editor.py"
else
    echo "✗ Installation failed!"
    exit 1
fi


