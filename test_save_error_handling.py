#!/usr/bin/env python3
"""
Test script to verify robust save error handling
"""

import sys
import os
import tempfile
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt6.QtCore import Qt

# Add src to path
sys.path.insert(0, 'src')

from main import SimpleEditorApplication

class SaveTestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Save Error Handling Test")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Instructions
        instructions = QLabel("""
        <h3>Save Error Handling Test</h3>
        <p>This test verifies that save failures don't crash the system.</p>
        <ol>
        <li><b>Test 1:</b> Try to save to a read-only location</li>
        <li><b>Test 2:</b> Try to save to a non-existent directory</li>
        <li><b>Test 3:</b> Try to save to a location without permissions</li>
        <li><b>Test 4:</b> Try to save to a valid location (should work)</li>
        </ol>
        <p><b>Expected:</b> All errors should be handled gracefully with helpful messages.</p>
        """)
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Create Simple Editor instance
        self.editor = SimpleEditorApplication()
        self.editor.setParent(self)
        layout.addWidget(self.editor)
        
        # Test buttons
        test_layout = QVBoxLayout()
        
        # Test 1: Read-only file
        btn1 = QPushButton("Test 1: Save to Read-Only File")
        btn1.clicked.connect(self.test_readonly_save)
        test_layout.addWidget(btn1)
        
        # Test 2: Non-existent directory
        btn2 = QPushButton("Test 2: Save to Non-Existent Directory")
        btn2.clicked.connect(self.test_nonexistent_dir_save)
        test_layout.addWidget(btn2)
        
        # Test 3: Valid save
        btn3 = QPushButton("Test 3: Save to Valid Location")
        btn3.clicked.connect(self.test_valid_save)
        test_layout.addWidget(btn3)
        
        layout.addLayout(test_layout)
        
        # Status label
        self.status_label = QLabel("Ready to test save error handling")
        layout.addWidget(self.status_label)
    
    def test_readonly_save(self):
        """Test saving to a read-only file"""
        try:
            # Create a temporary read-only file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                f.write("This is a read-only file")
                readonly_file = f.name
            
            # Make it read-only
            os.chmod(readonly_file, 0o444)
            
            # Try to save to it
            self.editor.current_file = readonly_file
            self.editor.text_editor.setPlainText("Trying to overwrite read-only file")
            self.editor.is_modified = True
            
            success = self.editor.save_file()
            self.status_label.setText(f"Read-only save test: {'SUCCESS' if success else 'FAILED (expected)'}")
            
            # Clean up
            try:
                os.remove(readonly_file)
            except:
                pass
                
        except Exception as e:
            self.status_label.setText(f"Read-only test error: {e}")
    
    def test_nonexistent_dir_save(self):
        """Test saving to a non-existent directory"""
        try:
            # Try to save to a non-existent directory
            nonexistent_file = "/nonexistent/directory/test.txt"
            self.editor.current_file = nonexistent_file
            self.editor.text_editor.setPlainText("Trying to save to non-existent directory")
            self.editor.is_modified = True
            
            success = self.editor.save_file()
            self.status_label.setText(f"Non-existent dir test: {'SUCCESS' if success else 'FAILED (expected)'}")
            
        except Exception as e:
            self.status_label.setText(f"Non-existent dir test error: {e}")
    
    def test_valid_save(self):
        """Test saving to a valid location"""
        try:
            # Create a temporary file
            with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.txt') as f:
                temp_file = f.name
            
            # Try to save to it
            self.editor.current_file = temp_file
            self.editor.text_editor.setPlainText("This is a test save")
            self.editor.is_modified = True
            
            success = self.editor.save_file()
            self.status_label.setText(f"Valid save test: {'SUCCESS' if success else 'FAILED'}")
            
            # Clean up
            try:
                os.remove(temp_file)
            except:
                pass
                
        except Exception as e:
            self.status_label.setText(f"Valid save test error: {e}")

def main():
    app = QApplication(sys.argv)
    window = SaveTestWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
