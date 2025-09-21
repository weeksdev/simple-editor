#!/usr/bin/env python3
"""
Test script for Simple Editor
"""

import sys
import os

# Add current directory to path for testing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_import():
    """Test that the module can be imported"""
    try:
        import simple_editor
        print("✓ Module import successful")
        return True
    except ImportError as e:
        print(f"✗ Module import failed: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality without GUI"""
    try:
        import tkinter as tk
        from simple_editor import SimpleEditor
        
        # Create a test root window (hidden)
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        # Create editor instance
        editor = SimpleEditor(root)
        
        # Test basic text operations
        editor.text_widget.insert("1.0", "Test text")
        content = editor.text_widget.get("1.0", "end-1c")
        
        if content == "Test text":
            print("✓ Basic text operations work")
        else:
            print("✗ Basic text operations failed")
            return False
        
        # Test paste plain functionality
        editor.root.clipboard_clear()
        editor.root.clipboard_append("Pasted text")
        editor.paste_plain()
        
        content = editor.text_widget.get("1.0", "end-1c")
        if "Pasted text" in content:
            print("✓ Paste plain functionality works")
        else:
            print("✗ Paste plain functionality failed")
            return False
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"✗ Basic functionality test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Running Simple Editor tests...")
    print("-" * 40)
    
    tests = [
        test_import,
        test_basic_functionality,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        print()
    
    print("-" * 40)
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed!")
        return 0
    else:
        print("✗ Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())


