#!/usr/bin/env python3
"""
Enterprise-level test suite for Simple Editor

This module provides comprehensive testing for the enterprise-level
Simple Editor application, including unit tests and integration tests.

Features:
- Component testing for all major modules
- Integration testing for application workflow
- Performance testing for animation and rendering
- Error handling validation
"""

import sys
import os
import unittest
from unittest.mock import Mock, patch, MagicMock
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import SimpleEditorApplication, create_application
from src.rainbow_border import RainbowBorderWidget
from src.text_editor import TextEditorWidget


class TestRainbowBorderWidget(unittest.TestCase):
    """Test suite for RainbowBorderWidget"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.widget = RainbowBorderWidget()
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.widget.close()
    
    def test_initialization(self):
        """Test widget initialization"""
        self.assertIsNotNone(self.widget)
        self.assertEqual(self.widget.border_width, 3)
        self.assertEqual(self.widget.animation_speed, 1.0)
        self.assertTrue(self.widget.animation_timer.isActive())
    
    def test_animation_speed_validation(self):
        """Test animation speed validation"""
        # Test valid speed
        self.widget.set_animation_speed(2.0)
        self.assertEqual(self.widget.animation_speed, 2.0)
        
        # Test invalid speed (too high)
        with self.assertRaises(ValueError):
            self.widget.set_animation_speed(15.0)
        
        # Test invalid speed (too low)
        with self.assertRaises(ValueError):
            self.widget.set_animation_speed(0.05)
    
    def test_border_width_validation(self):
        """Test border width validation"""
        # Test valid width
        self.widget.set_border_width(5)
        self.assertEqual(self.widget.border_width, 5)
        
        # Test invalid width (too high)
        with self.assertRaises(ValueError):
            self.widget.set_border_width(25)
        
        # Test invalid width (too low)
        with self.assertRaises(ValueError):
            self.widget.set_border_width(0)
    
    def test_animation_control(self):
        """Test animation start/stop functionality"""
        # Test stop animation
        self.widget.stop_animation()
        self.assertFalse(self.widget.animation_timer.isActive())
        
        # Test start animation
        self.widget.start_animation()
        self.assertTrue(self.widget.animation_timer.isActive())
    
    def test_paint_event(self):
        """Test paint event handling"""
        # This is a basic test - actual painting is hard to test without visual output
        self.widget.show()
        self.widget.update()
        # If no exception is raised, the test passes


class TestTextEditorWidget(unittest.TestCase):
    """Test suite for TextEditorWidget"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.widget = TextEditorWidget()
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.widget.close()
    
    def test_initialization(self):
        """Test widget initialization"""
        self.assertIsNotNone(self.widget)
        self.assertTrue(self.widget.isUndoRedoEnabled())
        self.assertEqual(self.widget.font().family(), "Monaco")
    
    def test_text_operations(self):
        """Test basic text operations"""
        # Test set and get text
        test_text = "Hello, World!"
        self.widget.set_plain_text(test_text)
        self.assertEqual(self.widget.get_plain_text(), test_text)
        
        # Test clear text
        self.widget.clear_text()
        self.assertEqual(self.widget.get_plain_text(), "")
    
    def test_zoom_operations(self):
        """Test zoom functionality"""
        initial_size = self.widget.font().pointSize()
        
        # Test zoom in
        self.widget.zoom_in()
        self.assertGreater(self.widget.font().pointSize(), initial_size)
        
        # Test zoom out
        self.widget.zoom_out()
        self.assertEqual(self.widget.font().pointSize(), initial_size)
        
        # Test reset zoom
        self.widget.reset_zoom()
        self.assertEqual(self.widget.font().pointSize(), 12)
    
    def test_font_change(self):
        """Test font change functionality"""
        # Mock the font dialog
        with patch('src.text_editor.QFontDialog.getFont') as mock_dialog:
            mock_dialog.return_value = (QFont("Arial", 14), True)
            
            result = self.widget.change_font()
            self.assertTrue(result)
            self.assertEqual(self.widget.font().family(), "Arial")
            self.assertEqual(self.widget.font().pointSize(), 14)
    
    def test_paste_plain_text(self):
        """Test plain text paste functionality"""
        # Mock clipboard
        mock_clipboard = Mock()
        mock_clipboard.text.return_value = "Test content"
        
        with patch.object(self.widget.parent(), 'clipboard', return_value=mock_clipboard):
            self.widget.paste_plain_text()
            # Verify text was inserted (basic check)
            self.assertIn("Test content", self.widget.get_plain_text())


class TestSimpleEditorApplication(unittest.TestCase):
    """Test suite for SimpleEditorApplication"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.window = SimpleEditorApplication()
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.window.close()
    
    def test_initialization(self):
        """Test application initialization"""
        self.assertIsNotNone(self.window)
        self.assertEqual(self.window.windowTitle(), "Simple Editor")
        self.assertIsNotNone(self.window.text_editor)
        self.assertIsNotNone(self.window.rainbow_border)
    
    def test_file_operations(self):
        """Test file operations"""
        # Test new file
        self.window.new_file()
        self.assertIsNone(self.window.current_file)
        self.assertFalse(self.window.is_modified)
        
        # Test text modification detection
        self.window.text_editor.set_plain_text("Test content")
        self.assertTrue(self.window.is_modified)
    
    def test_rainbow_border_controls(self):
        """Test rainbow border control functions"""
        # Test toggle border
        self.window.toggle_rainbow_border()
        self.assertFalse(self.window.toggle_border_action.isChecked())
        
        # Test speed controls
        initial_speed = self.window.rainbow_border.animation_speed
        self.window.speed_up_animation()
        self.assertGreater(self.window.rainbow_border.animation_speed, initial_speed)
        
        self.window.reset_animation_speed()
        self.assertEqual(self.window.rainbow_border.animation_speed, 1.0)
    
    def test_menu_creation(self):
        """Test menu bar creation"""
        menubar = self.window.menuBar()
        self.assertIsNotNone(menubar)
        
        # Check that main menus exist
        menu_titles = [menu.title() for menu in menubar.findChildren(type(menubar))]
        self.assertIn("File", menu_titles)
        self.assertIn("Edit", menu_titles)
        self.assertIn("View", menu_titles)


class TestApplicationIntegration(unittest.TestCase):
    """Integration tests for the complete application"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.app = QApplication.instance() or QApplication(sys.argv)
        self.window = SimpleEditorApplication()
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.window.close()
    
    def test_component_integration(self):
        """Test integration between components"""
        # Test that text editor is properly integrated
        self.assertIsNotNone(self.window.text_editor)
        
        # Test that rainbow border is properly integrated
        self.assertIsNotNone(self.window.rainbow_border)
        
        # Test that signals are connected
        self.window.text_editor.set_plain_text("Test")
        self.assertTrue(self.window.is_modified)
    
    def test_application_lifecycle(self):
        """Test application lifecycle"""
        # Test application creation
        app = create_application()
        self.assertIsNotNone(app)
        self.assertEqual(app.applicationName(), "Simple Editor")
    
    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test invalid file operations (should not crash)
        with patch('builtins.open', side_effect=IOError("Test error")):
            self.window.current_file = "test.txt"
            self.window.save_file()  # Should handle error gracefully


def run_performance_tests():
    """Run performance tests for animation and rendering"""
    print("Running performance tests...")
    
    app = QApplication.instance() or QApplication(sys.argv)
    
    # Test rainbow border performance
    border = RainbowBorderWidget()
    border.show()
    
    import time
    start_time = time.time()
    
    # Simulate animation updates
    for _ in range(100):
        border._update_animation()
        border.update()
    
    end_time = time.time()
    print(f"Animation performance: {end_time - start_time:.3f} seconds for 100 updates")
    
    border.close()


def main():
    """Main test runner"""
    print("Running Simple Editor Enterprise Test Suite")
    print("=" * 50)
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance tests
    run_performance_tests()
    
    print("\nTest suite completed!")


if __name__ == "__main__":
    main()
