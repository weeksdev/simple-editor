#!/bin/bash
# Create a macOS launcher for Simple Editor

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LAUNCHER_PATH="$SCRIPT_DIR/Simple Editor.app"

echo "Creating macOS launcher..."

# Create app bundle structure
mkdir -p "$LAUNCHER_PATH/Contents/MacOS"
mkdir -p "$LAUNCHER_PATH/Contents/Resources"

# Create Info.plist
cat > "$LAUNCHER_PATH/Contents/Info.plist" << EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleExecutable</key>
    <string>simple-editor</string>
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
    <string>10.15</string>
</dict>
</plist>
EOF

# Create the executable script
cat > "$LAUNCHER_PATH/Contents/MacOS/simple-editor" << EOF
#!/bin/bash
cd "$SCRIPT_DIR"

# Set TCL_LIBRARY path for tkinter
export TCL_LIBRARY="/opt/homebrew/lib/tcl8.6"
export TK_LIBRARY="/opt/homebrew/lib/tk8.6"

# Try to find TCL/TK libraries
if [ -d "/opt/homebrew/lib/tcl8.6" ]; then
    export TCL_LIBRARY="/opt/homebrew/lib/tcl8.6"
    export TK_LIBRARY="/opt/homebrew/lib/tk8.6"
elif [ -d "/usr/local/lib/tcl8.6" ]; then
    export TCL_LIBRARY="/usr/local/lib/tcl8.6"
    export TK_LIBRARY="/usr/local/lib/tk8.6"
fi

source .venv/bin/activate
python simple_editor_qt.py
EOF

chmod +x "$LAUNCHER_PATH/Contents/MacOS/simple-editor"

echo "✓ Launcher created at: $LAUNCHER_PATH"
echo "You can now drag 'Simple Editor.app' to your Applications folder"
