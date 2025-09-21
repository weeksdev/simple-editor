#!/bin/bash
# Simple macOS build script for Simple Editor
# This is much simpler and more reliable than the complex approach

set -e

echo "Building Simple Editor for macOS (simple approach)..."

# Clean previous builds
rm -rf dist build "Simple Editor.app" "Simple Editor-*.dmg"

# Create virtual environment
echo "Setting up build environment..."
python3 -m venv build_env
source build_env/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install PyQt6 PyInstaller Pillow

# Create icon (if not already created)
if [ ! -f "icon.icns" ]; then
    echo "Creating app icon..."
    python create_icon_optimized.py
else
    echo "Using existing icon.icns"
fi

# Build with PyInstaller using onefile mode (simpler)
echo "Building macOS app..."
pyinstaller --onefile --windowed \
  --name "Simple Editor" \
  --icon=icon.icns \
  --osx-bundle-identifier com.simpleeditor.app \
  --add-data "src:src" \
  --hidden-import PyQt6.QtCore \
  --hidden-import PyQt6.QtGui \
  --hidden-import PyQt6.QtWidgets \
  --hidden-import PyQt6.sip \
  simple_editor_enterprise.py

# Create proper .app bundle
echo "Creating app bundle..."
APP_NAME="Simple Editor.app"
mkdir -p "$APP_NAME/Contents/MacOS"
mkdir -p "$APP_NAME/Contents/Resources"

# Copy the executable
cp "dist/Simple Editor" "$APP_NAME/Contents/MacOS/Simple Editor"
chmod +x "$APP_NAME/Contents/MacOS/Simple Editor"

# Copy icon
if [ -f "icon.icns" ]; then
    cp "icon.icns" "$APP_NAME/Contents/Resources/"
fi

# Create Info.plist
cat > "$APP_NAME/Contents/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>Simple Editor</string>
    <key>CFBundleIdentifier</key>
    <string>com.simpleeditor.app</string>
    <key>CFBundleName</key>
    <string>Simple Editor</string>
    <key>CFBundleVersion</key>
    <string>1.0.0</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0.0</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleSignature</key>
    <string>????</string>
    <key>LSMinimumSystemVersion</key>
    <string>10.15.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSRequiresAquaSystemAppearance</key>
    <false/>
    <key>CFBundleDocumentTypes</key>
    <array>
        <dict>
            <key>CFBundleTypeName</key>
            <string>Text Document</string>
            <key>CFBundleTypeRole</key>
            <string>Editor</string>
            <key>LSItemContentTypes</key>
            <array>
                <string>public.text</string>
                <string>public.plain-text</string>
            </array>
            <key>CFBundleTypeExtensions</key>
            <array>
                <string>txt</string>
            </array>
        </dict>
    </array>
</dict>
</plist>
EOF

# Create DMG
echo "Creating DMG installer..."
DMG_DIR="Simple Editor DMG"
mkdir -p "$DMG_DIR"
cp -R "$APP_NAME" "$DMG_DIR/"
ln -s /Applications "$DMG_DIR/Applications"

DMG_NAME="Simple Editor-1.0.0.dmg"
hdiutil create -volname "Simple Editor" -srcfolder "$DMG_DIR" -ov -format UDZO "$DMG_NAME"

# Clean up
rm -rf "$DMG_DIR"

echo "✓ Build complete!"
echo "✓ DMG created: $DMG_NAME"
echo ""
echo "To install:"
echo "1. Open the DMG file"
echo "2. Drag 'Simple Editor.app' to your Applications folder"
echo "3. Launch from Applications or Spotlight"
