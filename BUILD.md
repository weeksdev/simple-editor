# Building Simple Editor

This document explains how to build Simple Editor for different platforms.

## macOS DMG Build

### Prerequisites
- macOS 10.15 or later
- Python 3.8 or later
- No Xcode required (uses simple build method)

### Quick Build
```bash
./build_simple.sh
```

This will create:
- `Simple Editor-1.0.0.dmg` - Installer package
- `Simple Editor.app` - Application bundle

### Manual Build Steps
1. Create virtual environment:
   ```bash
   python3 -m venv build_env
   source build_env/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install PyQt6
   ```

3. Create app icon:
   ```bash
   python create_icon.py
   ```

4. Run the build script:
   ```bash
   ./build_simple.sh
   ```

### Installation
1. Open the DMG file
2. Drag "Simple Editor.app" to your Applications folder
3. Launch from Applications or Spotlight

## GitHub Actions Build

The repository includes GitHub Actions workflows that automatically build DMG files when you create a release tag.

### Creating a Release
1. Create and push a tag:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. GitHub Actions will automatically:
   - Build the macOS DMG
   - Create a GitHub release
   - Upload the DMG file

### Manual Workflow Trigger
You can also trigger the build manually:
1. Go to Actions tab in GitHub
2. Select "Build macOS DMG"
3. Click "Run workflow"

## Build Artifacts

### macOS DMG
- **File**: `Simple Editor-{version}.dmg`
- **Size**: ~60MB (includes PyQt6)
- **Requirements**: macOS 10.15+
- **Dependencies**: None (self-contained)

### App Bundle Structure
```
Simple Editor.app/
├── Contents/
│   ├── MacOS/
│   │   └── Simple Editor (launcher script)
│   ├── Resources/
│   │   ├── simple_editor_qt.py
│   │   └── icon.icns
│   └── Info.plist
```

## Troubleshooting

### Build Issues
- **Python not found**: Ensure Python 3.8+ is installed
- **PyQt6 import error**: Run `pip install PyQt6` in virtual environment
- **Permission denied**: Run `chmod +x build_simple.sh`

### Runtime Issues
- **App won't launch**: Check that Python 3.8+ is installed on target system
- **Missing dependencies**: The app requires PyQt6 to be installed system-wide

### Alternative: PyInstaller Build
For a fully self-contained build (larger file size):
```bash
pip install PyInstaller
pyinstaller --onefile --windowed --name "Simple Editor" simple_editor_qt.py
```

## Development

### Local Development
```bash
# Install in development mode
pip install -e .

# Run directly
python simple_editor_qt.py

# Or use the launcher
./launch_editor.sh
```

### Testing
```bash
# Run tests
python test_editor.py

# Test paste functionality
python test_paste_content.py
```
