# Rainbow Border Toggle Fix

## Problem
When disabling the rainbow border using `Ctrl+R` or the View menu, the text editor would disappear completely. This happened because the toggle function was hiding the entire `RainbowBorderWidget` instead of just the border animation.

## Root Cause
The `toggle_rainbow_border()` method in `src/main.py` was calling:
- `self.rainbow_border.hide()` - This hid the entire widget
- `self.rainbow_border.show()` - This showed the entire widget

Since the text editor is a child widget inside the `RainbowBorderWidget`, hiding the parent also hid the text editor.

## Solution
Added border visibility control to the `RainbowBorderWidget` class:

### 1. Added Border Visibility State
```python
# In __init__ method
self.border_visible = True  # Whether the border should be drawn
```

### 2. Modified Paint Event
```python
def paintEvent(self, event) -> None:
    painter = QPainter(self)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    rect = self.rect()
    
    # Only draw the border if it's visible
    if self.border_visible:
        self._draw_gradient_border(painter, rect)
```

### 3. Added Control Methods
```python
def set_border_visible(self, visible: bool) -> None:
    """Set the border visibility"""
    self.border_visible = visible
    self.update()  # Trigger a repaint

def is_border_visible(self) -> bool:
    """Check if the border is currently visible"""
    return self.border_visible
```

### 4. Updated Toggle Function
```python
def toggle_rainbow_border(self) -> None:
    """Toggle rainbow border visibility"""
    if self.toggle_border_action.isChecked():
        self.rainbow_border.set_border_visible(True)
        self.rainbow_border.start_animation()
        self.status_bar.showMessage("Rainbow border enabled")
    else:
        self.rainbow_border.set_border_visible(False)
        self.rainbow_border.stop_animation()
        self.status_bar.showMessage("Rainbow border disabled")
```

## Result
- ✅ **Text editor remains visible** when border is disabled
- ✅ **Border animation stops** when disabled
- ✅ **Border reappears** when re-enabled
- ✅ **Animation resumes** when re-enabled
- ✅ **Status bar shows** appropriate messages
- ✅ **Build still works** perfectly

## Files Modified
- `src/rainbow_border.py` - Added border visibility control
- `src/main.py` - Updated toggle function to use new control

The rainbow border can now be toggled on/off without affecting the text editor visibility!
