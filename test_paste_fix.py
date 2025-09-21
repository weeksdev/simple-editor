#!/usr/bin/env python3
"""
Test script to verify paste functionality strips formatting
"""

import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard

class PasteTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Paste Test - Simple Editor")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Instructions
        instructions = QLabel("""
        <h3>Paste Test Instructions:</h3>
        <ol>
        <li>Copy some formatted text from a website or document (with bold, italic, colors, etc.)</li>
        <li>Click the "Test Paste" button below</li>
        <li>Check if the text appears as plain text without formatting</li>
        <li>Also try Ctrl+V directly in the text area</li>
        </ol>
        <p><b>Expected:</b> All formatting should be stripped, only plain text should appear.</p>
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Text editor (using our custom widget)
        from src.text_editor import TextEditorWidget
        self.text_editor = TextEditorWidget()
        self.text_editor.setPlainText("Paste formatted text here to test...")
        layout.addWidget(self.text_editor)
        
        # Test button
        test_button = QPushButton("Test Paste (Ctrl+V)")
        test_button.clicked.connect(self.test_paste)
        layout.addWidget(test_button)
        
        # Status label
        self.status_label = QLabel("Ready to test paste functionality")
        layout.addWidget(self.status_label)
    
    def test_paste(self):
        """Test the paste functionality"""
        try:
            # Get clipboard content
            clipboard = QApplication.clipboard()
            if clipboard.mimeData().hasText():
                text = clipboard.text()
                self.status_label.setText(f"Pasted: {text[:50]}{'...' if len(text) > 50 else ''}")
                
                # Test our custom paste method
                self.text_editor.paste_plain_text()
            else:
                self.status_label.setText("No text in clipboard")
        except Exception as e:
            self.status_label.setText(f"Error: {e}")

def main():
    app = QApplication(sys.argv)
    window = PasteTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
