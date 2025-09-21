#!/usr/bin/env python3
"""
Simple Text Editor - PyQt6 version
A fast, minimal text editor for macOS, Ubuntu, and Windows
Similar to Windows Notepad but with paste formatting stripped.
"""

import sys
import os
import math
from PyQt6.QtWidgets import (QApplication, QMainWindow, QTextEdit, QMenuBar, 
                            QMenu, QFileDialog, QMessageBox, QVBoxLayout, 
                            QWidget, QStatusBar, QFontDialog, QFrame)
from PyQt6.QtCore import Qt, QTimer, QPropertyAnimation, QEasingCurve
from PyQt6.QtGui import QAction, QKeySequence, QFont, QTextCursor, QPainter, QPen, QColor, QLinearGradient


class RainbowBorderWidget(QFrame):
    """Custom widget with animated rainbow border"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.animation_offset = 0
        self.border_width = 3  # Thinner, more subtle border
        self.animation_speed = 1  # Slower, more subtle animation
        self.wave_offset = 0  # Additional wave effect
        
        # Create animation timer
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self.update_animation)
        self.animation_timer.start(50)  # Slower update for more subtle effect
        
    def update_animation(self):
        """Update the animation offset with moving colors"""
        self.animation_offset = (self.animation_offset + self.animation_speed) % 360
        self.wave_offset = (self.wave_offset + 0.5) % 360  # Slower wave effect
        self.update()
    
    def paintEvent(self, event):
        """Paint the rainbow border with smooth gradients"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        rect = self.rect()
        
        # Create smooth gradient for each border side
        self.draw_gradient_border(painter, rect)
    
    def draw_gradient_border(self, painter, rect):
        """Draw smooth gradient borders on all sides with perfect alignment using rectangles"""
        # Draw each border as a filled rectangle for perfect alignment
        
        # Top border
        top_gradient = QLinearGradient(0, 0, rect.width(), 0)
        self.add_rainbow_stops(top_gradient, rect.width())
        painter.fillRect(0, 0, rect.width(), self.border_width, top_gradient)
        
        # Right border
        right_gradient = QLinearGradient(0, 0, 0, rect.height())
        self.add_rainbow_stops(right_gradient, rect.height())
        painter.fillRect(rect.width() - self.border_width, 0, 
                        self.border_width, rect.height(), right_gradient)
        
        # Bottom border
        bottom_gradient = QLinearGradient(rect.width(), 0, 0, 0)
        self.add_rainbow_stops(bottom_gradient, rect.width())
        painter.fillRect(0, rect.height() - self.border_width, 
                        rect.width(), self.border_width, bottom_gradient)
        
        # Left border
        left_gradient = QLinearGradient(0, rect.height(), 0, 0)
        self.add_rainbow_stops(left_gradient, rect.height())
        painter.fillRect(0, 0, self.border_width, rect.height(), left_gradient)
    
    def add_rainbow_stops(self, gradient, length):
        """Add subtle rainbow color stops to a gradient"""
        # Create a subtle rainbow with fewer stops for gentler effect
        num_stops = max(15, length // 15)  # Fewer stops for more subtle effect
        
        for i in range(num_stops):
            # Calculate position (0.0 to 1.0)
            position = i / (num_stops - 1) if num_stops > 1 else 0.5
            
            # Create subtle wave effects
            # Primary wave - moves around the border
            primary_hue = (self.animation_offset + position * 360) % 360
            
            # Subtle secondary wave - creates gentle rippling effect
            wave_effect = math.sin((position * 2 * math.pi) + (self.wave_offset * math.pi / 180)) * 10
            secondary_hue = (primary_hue + wave_effect) % 360
            
            # Very subtle shimmer effect
            shimmer_effect = math.sin((position * 4 * math.pi) + (self.animation_offset * math.pi / 90)) * 5
            final_hue = (secondary_hue + shimmer_effect) % 360
            
            # More subtle saturation and value variations
            saturation = int(120 + 30 * math.sin((position * math.pi) + (self.animation_offset * math.pi / 180)))
            value = int(180 + 20 * math.cos((position * math.pi * 1.5) + (self.wave_offset * math.pi / 120)))
            
            # Ensure values are within valid range for subtle effect
            saturation = max(100, min(150, saturation))
            value = max(160, min(200, value))
            
            # Ensure hue is within valid range (0-359)
            final_hue = int(final_hue) % 360
            
            # Create color with subtle properties
            color = QColor.fromHsv(final_hue, saturation, value)
            
            # Add stop to gradient
            gradient.setColorAt(position, color)


class SimpleEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_file = None
        self.is_modified = False
        
        self.init_ui()
        self.setup_shortcuts()
        
    def init_ui(self):
        """Initialize the user interface"""
        self.setWindowTitle("Simple Editor")
        self.setGeometry(100, 100, 800, 600)
        
        # Create rainbow border widget
        self.rainbow_border = RainbowBorderWidget()
        self.setCentralWidget(self.rainbow_border)
        
        # Create layout for content inside the border
        content_layout = QVBoxLayout(self.rainbow_border)
        content_layout.setContentsMargins(3, 3, 3, 3)  # Minimal margin for border
        
        # Create text editor
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Monaco", 12))
        self.text_edit.textChanged.connect(self.on_text_changed)
        content_layout.addWidget(self.text_edit)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Set focus to text editor
        self.text_edit.setFocus()
        
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu("File")
        
        new_action = QAction("New", self)
        new_action.setShortcut(QKeySequence.StandardKey.New)
        new_action.triggered.connect(self.new_file)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save As", self)
        save_as_action.setShortcut(QKeySequence("Ctrl+Shift+S"))
        save_as_action.triggered.connect(self.save_as_file)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu("Edit")
        
        undo_action = QAction("Undo", self)
        undo_action.setShortcut(QKeySequence.StandardKey.Undo)
        undo_action.triggered.connect(self.text_edit.undo)
        edit_menu.addAction(undo_action)
        
        redo_action = QAction("Redo", self)
        redo_action.setShortcut(QKeySequence.StandardKey.Redo)
        redo_action.triggered.connect(self.text_edit.redo)
        edit_menu.addAction(redo_action)
        
        edit_menu.addSeparator()
        
        cut_action = QAction("Cut", self)
        cut_action.setShortcut(QKeySequence.StandardKey.Cut)
        cut_action.triggered.connect(self.text_edit.cut)
        edit_menu.addAction(cut_action)
        
        copy_action = QAction("Copy", self)
        copy_action.setShortcut(QKeySequence.StandardKey.Copy)
        copy_action.triggered.connect(self.text_edit.copy)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction("Paste", self)
        paste_action.setShortcut(QKeySequence.StandardKey.Paste)
        paste_action.triggered.connect(self.paste_plain)
        edit_menu.addAction(paste_action)
        
        edit_menu.addSeparator()
        
        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.text_edit.selectAll)
        edit_menu.addAction(select_all_action)
        
        # View menu
        view_menu = menubar.addMenu("View")
        
        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence("Ctrl+="))
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)
        
        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence("Ctrl+-"))
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)
        
        reset_zoom_action = QAction("Reset Zoom", self)
        reset_zoom_action.setShortcut(QKeySequence("Ctrl+0"))
        reset_zoom_action.triggered.connect(self.reset_zoom)
        view_menu.addAction(reset_zoom_action)
        
        font_action = QAction("Font", self)
        font_action.triggered.connect(self.change_font)
        view_menu.addAction(font_action)
        
        view_menu.addSeparator()
        
        self.toggle_border_action = QAction("Toggle Rainbow Border", self)
        self.toggle_border_action.setCheckable(True)
        self.toggle_border_action.setChecked(True)
        self.toggle_border_action.setShortcut(QKeySequence("Ctrl+R"))
        self.toggle_border_action.triggered.connect(self.toggle_rainbow_border)
        view_menu.addAction(self.toggle_border_action)
        
        view_menu.addSeparator()
        
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
        
    def setup_shortcuts(self):
        """Setup additional keyboard shortcuts"""
        # Override paste to strip formatting
        self.text_edit.keyPressEvent = self.custom_key_press_event
        
    def custom_key_press_event(self, event):
        """Custom key press event to handle paste with formatting stripped"""
        if event.key() == Qt.Key.Key_V and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            self.paste_plain()
        else:
            # Call the original key press event
            QTextEdit.keyPressEvent(self.text_edit, event)
    
    def on_text_changed(self):
        """Handle text changes"""
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
    
    def update_title(self):
        """Update window title"""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title = f"Simple Editor - {filename}"
        else:
            title = "Simple Editor - Untitled"
        
        if self.is_modified:
            title += " *"
        
        self.setWindowTitle(title)
    
    def new_file(self):
        """Create a new file"""
        if self.check_save():
            self.text_edit.clear()
            self.current_file = None
            self.is_modified = False
            self.update_title()
    
    def open_file(self):
        """Open an existing file"""
        if self.check_save():
            file_path, _ = QFileDialog.getOpenFileName(
                self, "Open File", "", "Text files (*.txt);;All files (*.*)"
            )
            
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    self.text_edit.setPlainText(content)
                    self.current_file = file_path
                    self.is_modified = False
                    self.update_title()
                    
                except Exception as e:
                    QMessageBox.critical(self, "Error", f"Could not open file:\n{str(e)}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                content = self.text_edit.toPlainText()
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.is_modified = False
                self.update_title()
                self.status_bar.showMessage("File saved")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save the current file with a new name"""
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save As", "", "Text files (*.txt);;All files (*.*)"
        )
        
        if file_path:
            try:
                content = self.text_edit.toPlainText()
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.current_file = file_path
                self.is_modified = False
                self.update_title()
                self.status_bar.showMessage("File saved")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Could not save file:\n{str(e)}")
    
    def check_save(self):
        """Check if file needs to be saved before proceeding"""
        if self.is_modified:
            reply = QMessageBox.question(
                self, "Save Changes",
                "The file has been modified. Do you want to save changes?",
                QMessageBox.StandardButton.Yes | 
                QMessageBox.StandardButton.No | 
                QMessageBox.StandardButton.Cancel
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.save_file()
                return True
            elif reply == QMessageBox.StandardButton.No:
                return True
            else:
                return False
        
        return True
    
    def paste_plain(self):
        """Paste text without formatting"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        
        if text:
            # Insert plain text at current cursor position
            cursor = self.text_edit.textCursor()
            cursor.insertText(text)
    
    def zoom_in(self):
        """Increase font size"""
        current_font = self.text_edit.font()
        size = current_font.pointSize()
        if size < 72:  # Maximum font size
            current_font.setPointSize(size + 2)
            self.text_edit.setFont(current_font)
    
    def zoom_out(self):
        """Decrease font size"""
        current_font = self.text_edit.font()
        size = current_font.pointSize()
        if size > 6:  # Minimum font size
            current_font.setPointSize(size - 2)
            self.text_edit.setFont(current_font)
    
    def reset_zoom(self):
        """Reset font size to default"""
        font = QFont("Monaco", 12)
        self.text_edit.setFont(font)
    
    def change_font(self):
        """Change font"""
        current_font = self.text_edit.font()
        font, ok = QFontDialog.getFont(current_font, self)
        if ok:
            self.text_edit.setFont(font)
    
    def toggle_rainbow_border(self):
        """Toggle rainbow border visibility"""
        if self.toggle_border_action.isChecked():
            self.rainbow_border.show()
            self.rainbow_border.animation_timer.start(30)
        else:
            self.rainbow_border.hide()
            self.rainbow_border.animation_timer.stop()
    
    def speed_up_animation(self):
        """Increase animation speed"""
        self.rainbow_border.animation_speed = min(5, self.rainbow_border.animation_speed + 0.2)
        self.status_bar.showMessage(f"Animation speed: {self.rainbow_border.animation_speed:.1f}x")
    
    def slow_down_animation(self):
        """Decrease animation speed"""
        self.rainbow_border.animation_speed = max(0.2, self.rainbow_border.animation_speed - 0.2)
        self.status_bar.showMessage(f"Animation speed: {self.rainbow_border.animation_speed:.1f}x")
    
    def reset_animation_speed(self):
        """Reset animation speed to default"""
        self.rainbow_border.animation_speed = 1.0
        self.status_bar.showMessage("Animation speed reset to default")
    
    def closeEvent(self, event):
        """Handle window close event"""
        if self.check_save():
            event.accept()
        else:
            event.ignore()


def main():
    """Main function to run the application"""
    app = QApplication(sys.argv)
    app.setApplicationName("Simple Editor")
    app.setApplicationVersion("1.0.0")
    
    # Set application style
    app.setStyle('Fusion')  # Cross-platform style
    
    editor = SimpleEditor()
    editor.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
