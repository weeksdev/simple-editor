# Simple Editor

A professional, enterprise-level text editor for macOS, Ubuntu, and Windows - similar to Windows Notepad but with paste formatting stripped and a subtle animated rainbow border with flowing colors!

Built with enterprise architecture principles, featuring modular design, comprehensive documentation, and professional code organization.

## Features

### Core Functionality
- **Fast and lightweight** - Built with PyQt6 for optimal performance
- **Cross-platform** - Works on macOS, Ubuntu, and Windows
- **Plain text only** - Strips all formatting when pasting (like Windows Notepad)
- **Professional interface** - Clean, enterprise-level design focused on text editing

### Advanced Features
- **Standard shortcuts** - Cmd/Ctrl+N, O, S, V, etc.
- **Zoom support** - Zoom in/out with Cmd/Ctrl+Plus/Minus
- **Auto-save detection** - Prompts to save unsaved changes
- **Subtle rainbow border** - Gentle animated smooth gradient rainbow border with flowing colors (toggleable with Ctrl+R)
- **Font management** - Professional typography with font selection
- **Animation controls** - Adjustable rainbow border speed and effects

### Enterprise Architecture
- **Modular design** - Clean separation of concerns with professional abstractions
- **Comprehensive documentation** - Detailed docstrings and type hints
- **Error handling** - Robust error handling with user-friendly messages
- **Memory efficient** - Optimized rendering and resource management
- **Extensible** - Plugin-ready architecture for future enhancements

## Installation

### macOS DMG Installer (Recommended)

**Download the latest release:**
1. Go to [Releases](https://github.com/yourusername/simple-editor/releases)
2. Download `Simple Editor-{version}.dmg`
3. Open the DMG file
4. Drag "Simple Editor.app" to your Applications folder
5. Launch from Applications or Spotlight

**No Python dependencies required!** The DMG contains a self-contained app.

### Development Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/simple-editor.git
cd simple-editor

# Quick install with uv
./install_with_uv.sh

# Or manual installation
uv python install 3.12
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .
```

### Building from Source

See [BUILD.md](BUILD.md) for detailed build instructions.

**Quick build:**
```bash
./build_simple.sh
```

## Architecture

Simple Editor is built with enterprise-level architecture principles:

- **Modular Design**: Clean separation of concerns with professional abstractions
- **Type Safety**: Comprehensive type hints and validation
- **Documentation**: Detailed docstrings following Google style
- **Error Handling**: Robust error handling with graceful degradation
- **Performance**: Memory-efficient rendering and resource management

See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed technical documentation.

### Code Organization

```
src/
├── main.py                  # Main application and window management
├── rainbow_border.py        # Animated rainbow border widget
├── text_editor.py           # Advanced text editing widget
└── __init__.py             # Package initialization
```

## Usage

### Command line

```bash
simple-editor
```

### GUI launcher

```bash
simple-editor-gui
```

### Python module

```python
from simple_editor import main
main()
```

### macOS App Bundle

Create a native macOS app:

```bash
./create_launcher.sh
```

This creates `Simple Editor.app` that you can drag to your Applications folder.

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Cmd/Ctrl+N | New file |
| Cmd/Ctrl+O | Open file |
| Cmd/Ctrl+S | Save file |
| Cmd/Ctrl+Shift+S | Save as |
| Cmd/Ctrl+Z | Undo |
| Cmd/Ctrl+Shift+Z | Redo |
| Cmd/Ctrl+X | Cut |
| Cmd/Ctrl+C | Copy |
| Cmd/Ctrl+V | Paste (plain text only) |
| Cmd/Ctrl+A | Select all |
| Cmd/Ctrl+= | Zoom in |
| Cmd/Ctrl+- | Zoom out |
| Cmd/Ctrl+0 | Reset zoom |
| Cmd/Ctrl+R | Toggle rainbow border |
| Cmd/Ctrl+Shift+= | Speed up animation |
| Cmd/Ctrl+Shift+- | Slow down animation |
| Cmd/Ctrl+Shift+0 | Reset animation speed |
| Cmd/Ctrl+Q | Quit |

## System Requirements

- Python 3.8 or higher
- PyQt6 (automatically installed with the package)

### Installation Notes

**macOS:** No additional setup required - PyQt6 handles all dependencies automatically.

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pyqt6
```

**Windows:** PyQt6 installs automatically with pip/uv.

## Rainbow Border Animation

The subtle rainbow border features:

- **Flowing colors** - Colors gently move around the border perimeter
- **Subtle wave effects** - Gentle primary and secondary waves create soft patterns
- **Muted colors** - Lower saturation and brightness for a more professional look
- **Adjustable speed** - Control animation speed from 0.2x to 5x
- **Smooth gradients** - 15+ color stops for gentle transitions
- **Real-time control** - Toggle on/off and adjust speed while editing
- **Minimal border** - 3px thin border positioned directly against text area

## Why Simple Editor?

Simple Editor is designed to be the macOS equivalent of Windows Notepad - a fast, simple text editor that:

1. **Strips formatting on paste** - When you paste rich text, only the plain text is inserted
2. **No distractions** - Clean interface with no toolbars or complex features
3. **Fast startup** - Launches quickly for quick text editing tasks
4. **Cross-platform** - Same experience across macOS, Ubuntu, and Windows
5. **Fun and engaging** - Beautiful moving rainbow border makes editing more enjoyable

## Development

To run from source:

```bash
python simple_editor.py
```

## License

MIT License - see LICENSE file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.


