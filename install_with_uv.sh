#!/bin/bash
# Installation script for Simple Editor using uv

echo "Installing Simple Editor with uv..."

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "Error: uv is required but not installed."
    echo "Please install uv from https://github.com/astral-sh/uv"
    exit 1
fi

# Note: Using PyQt6 instead of tkinter to avoid TCL/TK dependency issues
echo "Using PyQt6 for cross-platform GUI (no TCL/TK dependencies required)"

# Install Python 3.12 with tkinter support
echo "Installing Python 3.12 with tkinter support..."
uv python install 3.12

# Create virtual environment
echo "Creating virtual environment..."
uv venv --python 3.12

# Activate virtual environment and install
echo "Installing Simple Editor..."
source .venv/bin/activate
uv pip install -e .

if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Simple Editor installed successfully!"
    echo ""
    echo "To run the editor:"
    echo "  source .venv/bin/activate"
    echo "  simple-editor"
    echo ""
    echo "Or run directly:"
    echo "  source .venv/bin/activate"
    echo "  python simple_editor.py"
    echo ""
    echo "To create a launcher script:"
    echo "  ./create_launcher.sh"
else
    echo "✗ Installation failed!"
    exit 1
fi
