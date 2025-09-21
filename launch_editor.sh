#!/bin/bash
# Simple launcher script for Simple Editor

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to the script directory
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

# Run the editor
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
    python simple_editor_qt.py
else
    python3 simple_editor_qt.py
fi


