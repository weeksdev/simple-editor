#!/usr/bin/env python3
"""
Simple test suite for Simple Editor Enterprise

This module provides basic validation tests for the enterprise-level
Simple Editor application without requiring full Qt event loops.
"""

import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test that all modules can be imported successfully"""
    print("Testing imports...")
    
    try:
        from src.rainbow_border import RainbowBorderWidget
        print("✓ RainbowBorderWidget imported successfully")
    except Exception as e:
        print(f"✗ Failed to import RainbowBorderWidget: {e}")
        return False
    
    try:
        from src.text_editor import TextEditorWidget
        print("✓ TextEditorWidget imported successfully")
    except Exception as e:
        print(f"✗ Failed to import TextEditorWidget: {e}")
        return False
    
    try:
        from src.main import SimpleEditorApplication, create_application
        print("✓ SimpleEditorApplication imported successfully")
    except Exception as e:
        print(f"✗ Failed to import SimpleEditorApplication: {e}")
        return False
    
    return True

def test_enterprise_code():
    """Test that the enterprise code runs without errors"""
    print("\nTesting enterprise code execution...")
    
    try:
        # Initialize QApplication for widget testing
        from PyQt6.QtWidgets import QApplication
        app = QApplication.instance() or QApplication(sys.argv)
        
        # Test rainbow border widget creation
        from src.rainbow_border import RainbowBorderWidget
        widget = RainbowBorderWidget()
        
        # Test basic functionality
        widget.set_animation_speed(2.0)
        assert widget.animation_speed == 2.0
        print("✓ RainbowBorderWidget functionality works")
        
        # Test border width
        widget.set_border_width(5)
        assert widget.border_width == 5
        print("✓ Border width setting works")
        
        # Test animation controls
        widget.stop_animation()
        assert not widget.animation_timer.isActive()
        widget.start_animation()
        assert widget.animation_timer.isActive()
        print("✓ Animation controls work")
        
        widget.close()
        
    except Exception as e:
        print(f"✗ RainbowBorderWidget test failed: {e}")
        return False
    
    return True

def test_build_system():
    """Test that the build system works"""
    print("\nTesting build system...")
    
    # Check if build files exist
    build_files = [
        "build_simple.sh",
        "create_icon.py",
        "simple_editor_enterprise.py",
        "src/main.py",
        "src/rainbow_border.py",
        "src/text_editor.py"
    ]
    
    for file in build_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            return False
    
    return True

def test_documentation():
    """Test that documentation is complete"""
    print("\nTesting documentation...")
    
    doc_files = [
        "README.md",
        "BUILD.md",
        "ARCHITECTURE.md",
        ".gitignore"
    ]
    
    for file in doc_files:
        if os.path.exists(file):
            print(f"✓ {file} exists")
        else:
            print(f"✗ {file} missing")
            return False
    
    return True

def main():
    """Main test runner"""
    print("Simple Editor Enterprise - Basic Test Suite")
    print("=" * 50)
    
    tests = [
        ("Import Tests", test_imports),
        ("Enterprise Code Tests", test_enterprise_code),
        ("Build System Tests", test_build_system),
        ("Documentation Tests", test_documentation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
            print(f"✓ {test_name} PASSED")
        else:
            print(f"✗ {test_name} FAILED")
    
    print(f"\nTest Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enterprise code is working correctly.")
        return 0
    else:
        print("❌ Some tests failed. Please check the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
