"""
Enterprise-level Text Editor Widget

This module provides a sophisticated text editing widget with advanced
features and professional functionality.

Features:
- Plain text paste with formatting stripped
- Advanced keyboard shortcuts and accessibility
- Professional font rendering and typography
- Memory-efficient text handling
- Cross-platform compatibility
"""

from typing import Optional, Callable
from PyQt6.QtWidgets import QTextEdit, QFontDialog
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QTextCursor, QKeySequence


class TextEditorWidget(QTextEdit):
    """
    Enterprise-level text editor widget with advanced features
    
    Provides a sophisticated text editing experience with professional
    functionality and optimal performance characteristics.
    
    Signals:
        text_changed: Emitted when text content changes
        font_changed: Emitted when font is changed
    """
    
    # Signal definitions
    text_changed = pyqtSignal()
    font_changed = pyqtSignal(QFont)
    
    # Default configuration
    DEFAULT_FONT_FAMILY = "Monaco"
    DEFAULT_FONT_SIZE = 12
    DEFAULT_TAB_WIDTH = 4  # characters
    
    def __init__(self, parent: Optional['QWidget'] = None):
        """
        Initialize the text editor widget
        
        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        
        # Configure widget properties
        self._configure_widget()
        
        # Setup font
        self._setup_font()
        
        # Connect signals
        self._connect_signals()
    
    def _configure_widget(self) -> None:
        """
        Configure widget properties for optimal performance
        
        Sets up the widget with appropriate flags and properties
        for professional text editing experience.
        """
        # Enable undo/redo functionality
        self.setUndoRedoEnabled(True)
        
        # Set word wrap for better text display
        self.setLineWrapMode(QTextEdit.LineWrapMode.WidgetWidth)
        
        # Configure tab width
        self.setTabStopDistance(self.DEFAULT_TAB_WIDTH * 8)  # 8 pixels per character
        
        # Set focus policy for keyboard interaction
        self.setFocusPolicy(Qt.FocusPolicy.StrongFocus)
        
        # Enable text selection
        self.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse |
            Qt.TextInteractionFlag.TextSelectableByKeyboard |
            Qt.TextInteractionFlag.TextEditable
        )
    
    def _setup_font(self) -> None:
        """
        Setup default font with professional typography
        
        Configures the font for optimal readability and professional appearance.
        """
        font = QFont(self.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
    
    def _connect_signals(self) -> None:
        """
        Connect internal signals for proper event handling
        
        Sets up signal connections for text changes and other events.
        """
        # Connect text change signal
        self.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self) -> None:
        """
        Handle text change events
        
        Emits the text_changed signal when text content is modified.
        """
        self.text_changed.emit()
    
    def paste_plain_text(self) -> None:
        """
        Paste text without formatting (plain text only)
        
        Implements the core functionality of stripping all formatting
        from pasted content, similar to Windows Notepad behavior.
        """
        try:
            # Get clipboard content as plain text
            clipboard = self.parent().clipboard() if self.parent() else None
            if not clipboard:
                return
            
            text = clipboard.text()
            
            if text:
                # Insert plain text at current cursor position
                cursor = self.textCursor()
                cursor.insertText(text)
                
        except Exception as e:
            # Log error in production (placeholder for logging system)
            print(f"Error pasting plain text: {e}")
    
    def change_font(self) -> bool:
        """
        Open font dialog and change font
        
        Returns:
            True if font was changed, False if cancelled
        """
        current_font = self.font()
        font, ok = QFontDialog.getFont(current_font, self)
        
        if ok:
            self.setFont(font)
            self.font_changed.emit(font)
            return True
        
        return False
    
    def zoom_in(self) -> None:
        """
        Increase font size for better readability
        
        Increases font size by 2 points with bounds checking.
        """
        current_font = self.font()
        size = current_font.pointSize()
        
        if size < 72:  # Maximum font size
            new_font = QFont(current_font)
            new_font.setPointSize(size + 2)
            self.setFont(new_font)
            self.font_changed.emit(new_font)
    
    def zoom_out(self) -> None:
        """
        Decrease font size for more content visibility
        
        Decreases font size by 2 points with bounds checking.
        """
        current_font = self.font()
        size = current_font.pointSize()
        
        if size > 6:  # Minimum font size
            new_font = QFont(current_font)
            new_font.setPointSize(size - 2)
            self.setFont(new_font)
            self.font_changed.emit(new_font)
    
    def reset_zoom(self) -> None:
        """
        Reset font size to default value
        
        Restores the font to the default size and family.
        """
        font = QFont(self.DEFAULT_FONT_FAMILY, self.DEFAULT_FONT_SIZE)
        font.setStyleHint(QFont.StyleHint.Monospace)
        self.setFont(font)
        self.font_changed.emit(font)
    
    def get_plain_text(self) -> str:
        """
        Get the current text content as plain text
        
        Returns:
            Current text content without formatting
        """
        return self.toPlainText()
    
    def set_plain_text(self, text: str) -> None:
        """
        Set the text content from plain text
        
        Args:
            text: Plain text content to set
        """
        self.setPlainText(text)
    
    def clear_text(self) -> None:
        """
        Clear all text content
        
        Removes all text from the editor.
        """
        self.clear()
    
    def select_all_text(self) -> None:
        """
        Select all text in the editor
        
        Selects all text content for operations like copy, cut, etc.
        """
        self.selectAll()
    
    def keyPressEvent(self, event) -> None:
        """
        Handle key press events with custom behavior
        
        Implements custom key handling for paste operations and other
        specialized functionality.
        
        Args:
            event: Key press event from Qt framework
        """
        # Handle paste with formatting stripped (both Ctrl+V and Cmd+V)
        if (event.key() == Qt.Key.Key_V and 
            (event.modifiers() & Qt.KeyboardModifier.ControlModifier or
             event.modifiers() & Qt.KeyboardModifier.MetaModifier)):
            self.paste_plain_text()
            return
        
        # Handle middle mouse button paste
        if event.key() == Qt.Key.Key_Insert and event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            self.paste_plain_text()
            return
        
        # Call parent implementation for other keys
        super().keyPressEvent(event)
    
    def insertFromMimeData(self, source) -> None:
        """
        Override paste behavior to always strip formatting
        
        This method is called whenever content is pasted, ensuring that
        all formatting is stripped regardless of the paste method used.
        
        Args:
            source: MIME data source containing the pasted content
        """
        if source.hasText():
            # Get plain text and insert it without formatting
            text = source.text()
            if text:
                cursor = self.textCursor()
                cursor.insertText(text)
        else:
            # If no text, call parent implementation
            super().insertFromMimeData(source)
    
    def mousePressEvent(self, event) -> None:
        """
        Handle mouse press events
        
        Implements custom mouse handling for paste operations.
        
        Args:
            event: Mouse press event from Qt framework
        """
        # Handle middle mouse button paste
        if event.button() == Qt.MouseButton.MiddleButton:
            self.paste_plain_text()
            return
        
        # Call parent implementation for other mouse events
        super().mousePressEvent(event)
