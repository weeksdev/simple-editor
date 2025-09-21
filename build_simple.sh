#!/bin/bash
# Simple build script for Simple Editor (no Xcode required)

set -e

echo "Building Simple Editor (simple method)..."

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
pip install PyQt6

# Create icon
echo "Creating app icon..."
python create_icon.py

# Create app bundle manually
echo "Creating app bundle..."
APP_NAME="Simple Editor.app"
rm -rf "$APP_NAME"

# Create app bundle structure
mkdir -p "$APP_NAME/Contents/MacOS"
mkdir -p "$APP_NAME/Contents/Resources"

# Create a simple launcher script
cat > "$APP_NAME/Contents/MacOS/Simple Editor" << 'EOF'
#!/bin/bash
# Simple Editor launcher

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Set Python path
export PYTHONPATH="$APP_DIR:$PYTHONPATH"

# Run the Python script
python3 "$APP_DIR/simple_editor_enterprise.py"
EOF

chmod +x "$APP_NAME/Contents/MacOS/Simple Editor"

# Create Info.plist
cat > "$APP_NAME/Contents/Info.plist" << EOF
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

# Copy icon if it exists
if [ -f "icon.icns" ]; then
    cp "icon.icns" "$APP_NAME/Contents/Resources/"
fi

# Copy Python files to Resources
cp simple_editor_enterprise.py "$APP_NAME/Contents/Resources/"
cp -r src "$APP_NAME/Contents/Resources/"

# Create DMG
echo "Creating DMG installer..."

# Create DMG directory structure
DMG_DIR="Simple Editor DMG"
rm -rf "$DMG_DIR"
mkdir -p "$DMG_DIR"

# Copy app to DMG directory
cp -R "$APP_NAME" "$DMG_DIR/"

# Create Applications symlink
ln -s /Applications "$DMG_DIR/Applications"

# Create DMG
DMG_NAME="Simple Editor-1.0.0.dmg"
rm -f "$DMG_NAME"

hdiutil create -volname "Simple Editor" -srcfolder "$DMG_DIR" -ov -format UDZO "$DMG_NAME"

# Clean up
rm -rf "$DMG_DIR"
rm -rf build_env

echo "✓ DMG created: $DMG_NAME"
echo "✓ Build complete!"
echo ""
echo "To install:"
echo "1. Open the DMG file"
echo "2. Drag 'Simple Editor.app' to your Applications folder"
echo "3. Launch from Applications or Spotlight"
