"""
Simple Editor - Main Application Module

This module contains the main application class and entry point for
the Simple Editor text editor application.

Features:
- Professional main window with menu system
- File operations (new, open, save, save as)
- Advanced text editing capabilities
- Rainbow border with animation controls
- Cross-platform compatibility
"""

import sys
import os
import shutil
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QMenu, QVBoxLayout, 
    QWidget, QStatusBar, QFileDialog, QMessageBox
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QKeySequence, QFont

from .rainbow_border import RainbowBorderWidget
from .text_editor import TextEditorWidget


class SimpleEditorApplication(QMainWindow):
    """
    Main application class for Simple Editor
    
    Provides the primary interface for the text editor with professional
    menu system, file operations, and advanced features.
    
    Attributes:
        current_file (Optional[str]): Path to currently open file
        is_modified (bool): Whether current file has unsaved changes
        text_editor (TextEditorWidget): Main text editing widget
        rainbow_border (RainbowBorderWidget): Animated border widget
        status_bar (QStatusBar): Status bar for user feedback
    """
    
    # Application metadata
    APP_NAME = "Simple Editor"
    APP_VERSION = "1.0.0"
    APP_ORGANIZATION = "Simple Editor Team"
    
    # File operations
    SUPPORTED_FILE_TYPES = [
        ("Text files", "*.txt"),
        ("All files", "*.*")
    ]
    
    def __init__(self, parent: Optional['QWidget'] = None):
        """
        Initialize the main application window
        
        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        
        # Initialize application state
        self.current_file: Optional[str] = None
        self.is_modified = False
        
        # Setup application properties
        self._setup_application()
        
        # Initialize UI components
        self._initialize_ui()
        
        # Setup menu system
        self._create_menu_bar()
        
        # Setup status bar
        self._create_status_bar()
        
        # Connect signals
        self._connect_signals()
        
        # Set focus to text editor
        self.text_editor.setFocus()
    
    def _setup_application(self) -> None:
        """
        Setup application properties and metadata
        
        Configures the application with proper metadata and window properties.
        """
        # Set application properties
        self.setWindowTitle(self.APP_NAME)
        self.setGeometry(100, 100, 800, 600)
        
        # Set minimum window size
        self.setMinimumSize(400, 300)
    
    def _initialize_ui(self) -> None:
        """
        Initialize the user interface components
        
        Creates and configures all UI components including the text editor
        and rainbow border widget.
        """
        # Create rainbow border widget as central widget
        self.rainbow_border = RainbowBorderWidget()
        self.setCentralWidget(self.rainbow_border)
        
        # Create layout for content inside the border
        content_layout = QVBoxLayout(self.rainbow_border)
        content_layout.setContentsMargins(3, 3, 3, 3)  # Minimal margin for border
        
        # Create text editor widget
        self.text_editor = TextEditorWidget()
        content_layout.addWidget(self.text_editor)
    
    def _create_menu_bar(self) -> None:
        """
        Create the professional menu bar system
        
        Sets up a comprehensive menu system with all standard text editor
        operations and advanced features.
        """
        menubar = self.menuBar()
        
        # File menu
        self._create_file_menu(menubar)
        
        # Edit menu
        self._create_edit_menu(menubar)
        
        # View menu
        self._create_view_menu(menubar)
    
    def _create_file_menu(self, menubar: QMenuBar) -> None:
        """
        Create the File menu with standard operations
        
        Args:
            menubar: Menu bar to add the File menu to
        """
        file_menu = menubar.addMenu("File")
        
        # New file action
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        # Open file action
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        # Save file action
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        # Save as file action
        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
    
    def _create_edit_menu(self, menubar: QMenuBar) -> None:
        """
        Create the Edit menu with text operations
        
        Args:
            menubar: Menu bar to add the Edit menu to
        """
        edit_menu = menubar.addMenu("Edit")
        
        # Undo action
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.text_editor.undo)
        edit_menu.addAction(undo_action)
        
        # Redo action
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.text_editor.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        # Cut action
        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.text_editor.cut)
        edit_menu.addAction(cut_action)
        
        # Copy action
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.text_editor.copy)
        edit_menu.addAction(copy_action)
        
        # Paste action (plain text)
        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.text_editor.paste_plain_text)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        # Select all action
        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.text_editor.select_all_text)
        edit_menu.addAction(select_all_action)
    
    def _create_view_menu(self, menubar: QMenuBar) -> None:
        """
        Create the View menu with display options
        
        Args:
            menubar: Menu bar to add the View menu to
        """
        view_menu = menubar.addMenu("View")
        
        # Zoom in action
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+="))
        zoom_in_action.triggered.connect(self.text_editor.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        # Zoom out action
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.text_editor.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        # Reset zoom action
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self.text_editor.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        view_menu.addSeparator()
        
        # Font action
        font_action = QAction("Font", self)
        font_action.triggered.connect(self.text_editor.change_font)
        view_menu.addAction(font_action)
        
        view_menu.addSeparator()
        
        # Rainbow border toggle action
        self.toggle_border_action = QAction("Toggle Rainbow Border", self)
        self.toggle_border_action.setCheckable(True)
        self.toggle_border_action.setChecked(True)
        self.toggle_border_action.setShortcut(QKeySequence("Ctrl+R"))
        self.toggle_border_action.triggered.connect(self.toggle_rainbow_border)
        view_menu.addAction(self.toggle_border_action)
        
        view_menu.addSeparator()
        
        # Animation speed controls
        speed_up_action = QAction("Speed Up Animation", self)
        speed_up_action.setShortcut(QKeySequence("Ctrl+Shift+="))
        speed_up_action.triggered.connect(self.speed_up_animation)
        view_menu.addAction(speed_up_action)
        
        speed_down_action = QAction("Slow Down Animation", self)
        speed_down_action.setShortcut(QKeySequence("Ctrl+Shift+-"))
        speed_down_action.triggered.connect(self.slow_down_animation)
        view_menu.addAction(speed_down_action)
        
        reset_speed_action = QAction("Reset Animation Speed", self)
        reset_speed_action.setShortcut(QKeySequence("Ctrl+Shift+0"))
        reset_speed_action.triggered.connect(self.reset_animation_speed)
        view_menu.addAction(reset_speed_action)
    
    def _create_status_bar(self) -> None:
        """
        Create the status bar for user feedback
        
        Sets up a status bar to display application state and user feedback.
        """
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
    
    def _connect_signals(self) -> None:
        """
        Connect internal signals for proper event handling
        
        Sets up signal connections between components for coordinated behavior.
        """
        # Connect text editor signals
        self.text_editor.text_changed.connect(self._on_text_changed)
        self.text_editor.font_changed.connect(self._on_font_changed)
    
    def _on_text_changed(self) -> None:
        """
        Handle text change events
        
        Updates the application state when text content is modified.
        """
        if not self.is_modified:
            self.is_modified = True
            self._update_title()
    
    def _on_font_changed(self, font: QFont) -> None:
        """
        Handle font change events
        
        Args:
            font: New font that was selected
        """
        self.status_bar.showMessage(f"Font changed to {font.family()}, {font.pointSize()}pt")
    
    def _update_title(self) -> None:
        """
        Update the window title with current file and modification status
        
        Displays the current file name and modification indicator in the title bar.
        """
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title = f"{self.APP_NAME} - {filename}"
        else:
            title = f"{self.APP_NAME} - Untitled"
        
        if self.is_modified:
            title += " *"
        
        self.setWindowTitle(title)
    
    def new_file(self) -> None:
        """
        Create a new file
        
        Prompts to save current file if modified, then creates a new empty document.
        """
        if self._check_save():
            self.text_editor.clear_text()
            self.current_file = None
            self.is_modified = False
            self._update_title()
            self.status_bar.showMessage("New file created")
    
    def open_file(self) -> None:
        """
        Open an existing file
        
        Prompts to save current file if modified, then opens a file dialog
        to select and load a new file.
        """
        if self._check_save():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", 
                ";;".join([f"{desc} ({pattern})" for desc, pattern in self.SUPPORTED_FILE_TYPES])
            )
            
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    self.text_editor.set_plain_text(content)
                    self.current_file = file_path
                    self.is_modified = False
                    self._update_title()
                    self.status_bar.showMessage(f"Opened {os.path.basename(file_path)}")
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not open file:\n{str(e)}")
    
    def save_file(self) -> bool:
        """
        Save the current file with comprehensive error handling
        
        Saves to current file if available, otherwise prompts for save as.
        
        Returns:
            True if save was successful, False if failed or cancelled
        """
        if self.current_file:
            return self._perform_save(self.current_file)
        else:
            return self.save_as_file()
    
    def _perform_save(self, file_path: str) -> bool:
        """
        Perform the actual save operation with robust error handling
        
        Args:
            file_path: Path where to save the file
            
        Returns:
            True if save was successful, False if failed
        """
        try:
            # Validate file path
            if not file_path or not isinstance(file_path, str):
                raise ValueError("Invalid file path")
            
            # Check if directory exists and is writable
            directory = os.path.dirname(file_path)
            if directory and not os.path.exists(directory):
                raise FileNotFoundError(f"Directory does not exist: {directory}")
            
            if directory and not os.access(directory, os.W_OK):
                raise PermissionError(f"No write permission for directory: {directory}")
            
            # Get content safely
            try:
                content = self.text_editor.get_plain_text()
                if content is None:
                    content = ""
            except Exception as e:
                raise RuntimeError(f"Failed to get text content: {str(e)}")
            
            # Create backup if file exists
            backup_path = None
            if os.path.exists(file_path):
                try:
                    backup_path = f"{file_path}.backup"
                    shutil.copy2(file_path, backup_path)
                except Exception:
                    # Backup creation failed, but continue with save
                    pass
            
            # Perform atomic save
            temp_path = f"{file_path}.tmp"
            try:
                with open(temp_path, 'w', encoding='utf-8', newline='') as file:
                    file.write(content)
                
                # Atomic move
                if os.name == 'nt':  # Windows
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    os.rename(temp_path, file_path)
                else:  # Unix-like
                    os.rename(temp_path, file_path)
                
                # Remove backup if save was successful
                if backup_path and os.path.exists(backup_path):
                    try:
                        os.remove(backup_path)
                    except Exception:
                        pass
                
                # Update state
                self.is_modified = False
                self._update_title()
                self.status_bar.showMessage(f"Saved {os.path.basename(file_path)}")
                return True
                
            except Exception as e:
                # Restore backup if save failed
                if backup_path and os.path.exists(backup_path):
                    try:
                        shutil.copy2(backup_path, file_path)
                        os.remove(backup_path)
                    except Exception:
                        pass
                
                # Clean up temp file
                if os.path.exists(temp_path):
                    try:
                        os.remove(temp_path)
                    except Exception:
                        pass
                
                raise e
                
        except PermissionError as e:
            QMessageBox.critical(
                self, "Permission Denied", 
                f"Cannot save file: Permission denied\n\n{str(e)}\n\n"
                f"Please check:\n"
                f"• File is not read-only\n"
                f"• You have write permissions\n"
                f"• File is not open in another application"
            )
            return False
            
        except FileNotFoundError as e:
            QMessageBox.critical(
                self, "Directory Not Found", 
                f"Cannot save file: Directory not found\n\n{str(e)}\n\n"
                f"Please select a different location."
            )
            return False
            
        except OSError as e:
            QMessageBox.critical(
                self, "System Error", 
                f"Cannot save file: System error\n\n{str(e)}\n\n"
                f"Please try:\n"
                f"• Saving to a different location\n"
                f"• Checking available disk space\n"
                f"• Restarting the application"
            )
            return False
            
        except Exception as e:
            QMessageBox.critical(
                self, "Save Error", 
                f"An unexpected error occurred while saving:\n\n{str(e)}\n\n"
                f"Please try:\n"
                f"• Saving to a different location\n"
                f"• Restarting the application\n"
                f"• Contact support if the problem persists"
            )
            return False
    
    def save_as_file(self) -> bool:
        """
        Save the current file with a new name
        
        Opens a file dialog to select a new location and filename.
        
        Returns:
            True if save was successful, False if failed or cancelled
        """
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save As", "",
            ";;".join([f"{desc} ({pattern})" for desc, pattern in self.SUPPORTED_FILE_TYPES])
        )
        
        if file_path:
            success = self._perform_save(file_path)
            if success:
                self.current_file = file_path
                self.status_bar.showMessage(f"Saved as {os.path.basename(file_path)}")
            return success
        else:
            return False
    
    def _check_save(self) -> bool:
        """
        Check if file needs to be saved before proceeding
        
        Returns:
            True if operation can proceed, False if cancelled
        """
        if self.is_modified:
            reply = QMessageBox.question(
                self, "Save Changes",
                "The file has been modified. Do you want to save changes?",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                success = self.save_file()
                return success  # Only proceed if save was successful
            elif reply == QMessageBox.StandardButton.No:
                return True
            else:
                return False
        
        return True
    
    def toggle_rainbow_border(self) -> None:
        """
        Toggle rainbow border visibility
        
        Shows or hides the animated rainbow border based on current state.
        """
        if self.toggle_border_action.isChecked():
            self.rainbow_border.set_border_visible(True)
            self.rainbow_border.start_animation()
            self.status_bar.showMessage("Rainbow border enabled")
        else:
            self.rainbow_border.set_border_visible(False)
            self.rainbow_border.stop_animation()
            self.status_bar.showMessage("Rainbow border disabled")
    
    def speed_up_animation(self) -> None:
        """
        Increase animation speed
        
        Increases the rainbow border animation speed with bounds checking.
        """
        current_speed = self.rainbow_border.animation_speed
        new_speed = min(10.0, current_speed + 0.2)
        self.rainbow_border.set_animation_speed(new_speed)
        self.status_bar.showMessage(f"Animation speed: {new_speed:.1f}x")
    
    def slow_down_animation(self) -> None:
        """
        Decrease animation speed
        
        Decreases the rainbow border animation speed with bounds checking.
        """
        current_speed = self.rainbow_border.animation_speed
        new_speed = max(0.1, current_speed - 0.2)
        self.rainbow_border.set_animation_speed(new_speed)
        self.status_bar.showMessage(f"Animation speed: {new_speed:.1f}x")
    
    def reset_animation_speed(self) -> None:
        """
        Reset animation speed to default
        
        Restores the rainbow border animation speed to the default value.
        """
        self.rainbow_border.set_animation_speed(1.0)
        self.status_bar.showMessage("Animation speed reset to default")
    
    def closeEvent(self, event) -> None:
        """
        Handle window close event
        
        Prompts to save changes before closing the application.
        
        Args:
            event: Close event from Qt framework
        """
        if self._check_save():
            event.accept()
        else:
            event.ignore()


def create_application() -> QApplication:
    """
    Create and configure the QApplication instance
    
    Returns:
        Configured QApplication instance
    """
    app = QApplication(sys.argv)
    app.setApplicationName(SimpleEditorApplication.APP_NAME)
    app.setApplicationVersion(SimpleEditorApplication.APP_VERSION)
    app.setOrganizationName(SimpleEditorApplication.APP_ORGANIZATION)
    
    # Set application style for cross-platform consistency
    app.setStyle('Fusion')
    
    return app


def main() -> int:
    """
    Main entry point for the application
    
    Returns:
        Exit code (0 for success)
    """
    # Create application instance
    app = create_application()
    
    # Create main window
    window = SimpleEditorApplication()
    window.show()
    
    # Run application event loop
    return app.exec()


if __name__ == "__main__":
    sys.exit(main())
