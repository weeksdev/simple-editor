#!/usr/bin/env python3
"""
Test script to demonstrate what happens when pasting formatted content
into the Simple Editor
"""

import sys
from PyQt6.QtWidgets import QApplication, QTextEdit, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QClipboard, QFont

class PasteTestWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Paste Content Test - Simple Editor")
        self.setGeometry(100, 100, 800, 600)
        
        layout = QVBoxLayout()
        
        # Instructions
        instructions = QLabel("""
        <h3>Paste Content Test</h3>
        <p>This demonstrates what happens when you paste different types of formatted content:</p>
        <ol>
        <li>Copy some HTML table content from a webpage</li>
        <li>Copy some rich text from Word/Google Docs</li>
        <li>Copy some formatted text with bold/italic</li>
        <li>Click the buttons below to test different content types</li>
        </ol>
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Test buttons
        self.html_table_btn = QPushButton("Test HTML Table Content")
        self.html_table_btn.clicked.connect(self.test_html_table)
        layout.addWidget(self.html_table_btn)
        
        self.rich_text_btn = QPushButton("Test Rich Text Content")
        self.rich_text_btn.clicked.connect(self.test_rich_text)
        layout.addWidget(self.rich_text_btn)
        
        self.formatted_btn = QPushButton("Test Formatted Text")
        self.formatted_btn.clicked.connect(self.test_formatted_text)
        layout.addWidget(self.formatted_btn)
        
        # Text editor (simulates our Simple Editor)
        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Monaco", 12))
        layout.addWidget(self.text_edit)
        
        # Plain text paste button (like our Simple Editor)
        self.paste_plain_btn = QPushButton("Paste as Plain Text (like Simple Editor)")
        self.paste_plain_btn.clicked.connect(self.paste_plain)
        layout.addWidget(self.paste_plain_btn)
        
        # Regular paste button (for comparison)
        self.paste_rich_btn = QPushButton("Paste with Formatting (for comparison)")
        self.paste_rich_btn.clicked.connect(self.paste_rich)
        layout.addWidget(self.paste_rich_btn)
        
        self.setLayout(layout)
    
    def test_html_table(self):
        """Test with HTML table content"""
        html_content = """
        <table border="1">
        <tr>
            <th>Name</th>
            <th>Age</th>
            <th>City</th>
        </tr>
        <tr>
            <td><b>John Doe</b></td>
            <td>25</td>
            <td><i>New York</i></td>
        </tr>
        <tr>
            <td><b>Jane Smith</b></td>
            <td>30</td>
            <td><i>Los Angeles</i></td>
        </tr>
        </table>
        """
        
        # Set clipboard content
        clipboard = QApplication.clipboard()
        clipboard.setText(html_content)
        
        self.text_edit.append("=== HTML Table Content ===")
        self.text_edit.append("Original HTML:")
        self.text_edit.append(html_content)
        self.text_edit.append("\n" + "="*50 + "\n")
    
    def test_rich_text(self):
        """Test with rich text content"""
        rich_text = """
        This is **bold text** and this is *italic text*.
        
        Here's a list:
        1. First item
        2. Second item
        3. Third item
        
        And some code: `print("Hello World")`
        """
        
        clipboard = QApplication.clipboard()
        clipboard.setText(rich_text)
        
        self.text_edit.append("=== Rich Text Content ===")
        self.text_edit.append("Original Rich Text:")
        self.text_edit.append(rich_text)
        self.text_edit.append("\n" + "="*50 + "\n")
    
    def test_formatted_text(self):
        """Test with formatted text"""
        formatted_text = """
        Title: My Document
        Author: Test User
        Date: 2024-01-01
        
        This is a sample document with various formatting:
        - Bold text
        - Italic text
        - Underlined text
        - Different font sizes
        - Colors
        """
        
        clipboard = QApplication.clipboard()
        clipboard.setText(formatted_text)
        
        self.text_edit.append("=== Formatted Text Content ===")
        self.text_edit.append("Original Formatted Text:")
        self.text_edit.append(formatted_text)
        self.text_edit.append("\n" + "="*50 + "\n")
    
    def paste_plain(self):
        """Paste as plain text (like our Simple Editor)"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        
        self.text_edit.append("=== PASTED AS PLAIN TEXT ===")
        self.text_edit.append("Result (all formatting stripped):")
        self.text_edit.append(text)
        self.text_edit.append("\n" + "="*50 + "\n")
    
    def paste_rich(self):
        """Paste with formatting (for comparison)"""
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        
        self.text_edit.append("=== PASTED WITH FORMATTING ===")
        self.text_edit.append("Result (formatting preserved):")
        self.text_edit.append(text)
        self.text_edit.append("\n" + "="*50 + "\n")

def main():
    app = QApplication(sys.argv)
    widget = PasteTestWidget()
    widget.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
