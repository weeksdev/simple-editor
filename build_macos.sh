#!/bin/bash
# Build script for Simple Editor macOS DMG

set -e

echo "Building Simple Editor for macOS..."

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "Error: This script must be run on macOS"
    exit 1
fi

# Create virtual environment
echo "Creating virtual environment..."
python3 -m venv build_env
source build_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install PyQt6 PyInstaller

# Create icon
echo "Creating app icon..."
python create_icon.py

# Build the app
echo "Building macOS app bundle..."
pyinstaller simple_editor.spec

# Create DMG
echo "Creating DMG installer..."

# Create DMG directory structure
DMG_DIR="Simple Editor DMG"
rm -rf "$DMG_DIR"
mkdir -p "$DMG_DIR"

# Copy app to DMG directory
cp -R "dist/Simple Editor.app" "$DMG_DIR/"

# Create Applications symlink
ln -s /Applications "$DMG_DIR/Applications"

# Create DMG
DMG_NAME="Simple Editor-1.0.0.dmg"
rm -f "$DMG_NAME"

hdiutil create -volname "Simple Editor" -srcfolder "$DMG_DIR" -ov -format UDZO "$DMG_NAME"

# Clean up
rm -rf "$DMG_DIR"
rm -rf build_env
rm -rf build
rm -rf dist

echo "✓ DMG created: $DMG_NAME"
echo "✓ Build complete!"
