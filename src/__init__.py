"""
Simple Editor - Enterprise Text Editor Package

A professional, cross-platform text editor with subtle animated rainbow border.
Built with PyQt6 for optimal performance and native feel across platforms.

Author: Simple Editor Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Simple Editor Team"
__email__ = "team@simpleeditor.app"
__license__ = "MIT"

from .main import SimpleEditorApplication
from .rainbow_border import RainbowBorderWidget
from .text_editor import TextEditorWidget

__all__ = [
    "SimpleEditorApplication",
    "RainbowBorderWidget", 
    "TextEditorWidget",
]
