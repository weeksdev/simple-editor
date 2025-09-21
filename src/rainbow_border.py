"""
Enterprise-level Rainbow Border Widget

This module provides a sophisticated, animated rainbow border widget with
professional design principles and optimal performance characteristics.

Features:
- Smooth gradient animations with mathematical precision
- Configurable animation speed and visual effects
- Memory-efficient rendering with proper resource management
- Cross-platform compatibility with PyQt6
"""

import math
from typing import Optional
from PyQt6.QtWidgets import QFrame
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QPainter, QPen, QColor, QLinearGradient


class RainbowBorderWidget(QFrame):
    """
    Enterprise-level animated rainbow border widget
    
    Provides a sophisticated, animated rainbow border with smooth gradients
    and professional visual effects. Designed for optimal performance and
    memory efficiency.
    
    Attributes:
        animation_offset (int): Current animation position (0-360 degrees)
        border_width (int): Width of the border in pixels
        animation_speed (float): Speed multiplier for animation (0.1-10.0)
        wave_offset (int): Secondary wave effect offset
        animation_timer (QTimer): Timer for smooth animation updates
    """
    
    # Animation configuration constants
    DEFAULT_BORDER_WIDTH = 3
    DEFAULT_ANIMATION_SPEED = 1.0
    ANIMATION_UPDATE_INTERVAL = 50  # milliseconds
    MAX_ANIMATION_SPEED = 10.0
    MIN_ANIMATION_SPEED = 0.1
    
    # Color configuration for subtle, professional appearance
    COLOR_SATURATION_RANGE = (100, 150)  # Subtle saturation range
    COLOR_VALUE_RANGE = (160, 200)       # Professional brightness range
    WAVE_AMPLITUDE_PRIMARY = 10          # Primary wave effect amplitude
    WAVE_AMPLITUDE_SECONDARY = 5         # Secondary shimmer effect amplitude
    
    def __init__(self, parent: Optional['QWidget'] = None):
        """
        Initialize the rainbow border widget
        
        Args:
            parent: Parent widget (optional)
        """
        super().__init__(parent)
        
        # Initialize animation state
        self.animation_offset = 0
        self.wave_offset = 0
        self.border_width = self.DEFAULT_BORDER_WIDTH
        self.animation_speed = self.DEFAULT_ANIMATION_SPEED
        
        # Setup animation timer for smooth updates
        self._setup_animation_timer()
        
        # Configure widget properties
        self._configure_widget()
    
    def _setup_animation_timer(self) -> None:
        """
        Initialize and configure the animation timer
        
        Sets up a high-precision timer for smooth animation updates
        with proper resource management.
        """
        self.animation_timer = QTimer()
        self.animation_timer.timeout.connect(self._update_animation)
        self.animation_timer.start(self.ANIMATION_UPDATE_INTERVAL)
    
    def _configure_widget(self) -> None:
        """
        Configure widget properties for optimal performance
        
        Sets up the widget with appropriate flags and properties
        for smooth rendering and efficient updates.
        """
        # Enable mouse tracking for potential future interactions
        self.setMouseTracking(True)
        
        # Set minimum size to prevent layout issues
        self.setMinimumSize(100, 100)
    
    def _update_animation(self) -> None:
        """
        Update animation state for smooth color transitions
        
        Calculates new animation offsets using precise mathematical
        functions for smooth, continuous color flow.
        """
        # Update primary animation offset with speed control
        self.animation_offset = (self.animation_offset + self.animation_speed) % 360
        
        # Update secondary wave offset for shimmer effect
        self.wave_offset = (self.wave_offset + 0.5) % 360
        
        # Trigger repaint for smooth animation
        self.update()
    
    def set_animation_speed(self, speed: float) -> None:
        """
        Set animation speed with bounds checking
        
        Args:
            speed: Animation speed multiplier (0.1-10.0)
            
        Raises:
            ValueError: If speed is outside valid range
        """
        if not (self.MIN_ANIMATION_SPEED <= speed <= self.MAX_ANIMATION_SPEED):
            raise ValueError(
                f"Animation speed must be between {self.MIN_ANIMATION_SPEED} "
                f"and {self.MAX_ANIMATION_SPEED}"
            )
        
        self.animation_speed = speed
    
    def set_border_width(self, width: int) -> None:
        """
        Set border width with validation
        
        Args:
            width: Border width in pixels (1-20)
            
        Raises:
            ValueError: If width is outside valid range
        """
        if not (1 <= width <= 20):
            raise ValueError("Border width must be between 1 and 20 pixels")
        
        self.border_width = width
        self.update()
    
    def start_animation(self) -> None:
        """Start the animation timer"""
        if not self.animation_timer.isActive():
            self.animation_timer.start(self.ANIMATION_UPDATE_INTERVAL)
    
    def stop_animation(self) -> None:
        """Stop the animation timer"""
        self.animation_timer.stop()
    
    def paintEvent(self, event) -> None:
        """
        Paint the rainbow border with enterprise-level rendering
        
        Implements sophisticated gradient rendering with mathematical
        precision for smooth, professional visual effects.
        
        Args:
            event: Paint event from Qt framework
        """
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get widget dimensions
        rect = self.rect()
        
        # Render the gradient border
        self._draw_gradient_border(painter, rect)
    
    def _draw_gradient_border(self, painter: QPainter, rect) -> None:
        """
        Draw the gradient border with mathematical precision
        
        Creates smooth, professional gradients using advanced mathematical
        functions for optimal visual quality.
        
        Args:
            painter: QPainter instance for rendering
            rect: Widget rectangle for border positioning
        """
        # Draw each border side with optimized gradient rendering
        self._draw_top_border(painter, rect)
        self._draw_right_border(painter, rect)
        self._draw_bottom_border(painter, rect)
        self._draw_left_border(painter, rect)
    
    def _draw_top_border(self, painter: QPainter, rect) -> None:
        """Draw the top border with horizontal gradient"""
        gradient = QLinearGradient(0, 0, rect.width(), 0)
        self._add_rainbow_stops(gradient, rect.width())
        painter.fillRect(0, 0, rect.width(), self.border_width, gradient)
    
    def _draw_right_border(self, painter: QPainter, rect) -> None:
        """Draw the right border with vertical gradient"""
        gradient = QLinearGradient(0, 0, 0, rect.height())
        self._add_rainbow_stops(gradient, rect.height())
        painter.fillRect(
            rect.width() - self.border_width, 0,
            self.border_width, rect.height(), gradient
        )
    
    def _draw_bottom_border(self, painter: QPainter, rect) -> None:
        """Draw the bottom border with reverse horizontal gradient"""
        gradient = QLinearGradient(rect.width(), 0, 0, 0)
        self._add_rainbow_stops(gradient, rect.width())
        painter.fillRect(
            0, rect.height() - self.border_width,
            rect.width(), self.border_width, gradient
        )
    
    def _draw_left_border(self, painter: QPainter, rect) -> None:
        """Draw the left border with reverse vertical gradient"""
        gradient = QLinearGradient(0, rect.height(), 0, 0)
        self._add_rainbow_stops(gradient, rect.height())
        painter.fillRect(0, 0, self.border_width, rect.height(), gradient)
    
    def _add_rainbow_stops(self, gradient: QLinearGradient, length: int) -> None:
        """
        Add sophisticated rainbow color stops with mathematical precision
        
        Creates smooth color transitions using advanced mathematical functions
        for professional visual quality.
        
        Args:
            gradient: QLinearGradient to add color stops to
            length: Length of the gradient for stop calculation
        """
        # Calculate optimal number of stops for smooth gradients
        num_stops = max(15, length // 15)
        
        for i in range(num_stops):
            # Calculate position with mathematical precision
            position = i / (num_stops - 1) if num_stops > 1 else 0.5
            
            # Calculate hue with multiple wave effects
            hue = self._calculate_hue(position)
            
            # Calculate saturation and value with professional ranges
            saturation = self._calculate_saturation(position)
            value = self._calculate_value(position)
            
            # Create color with validated parameters
            color = QColor.fromHsv(int(hue), saturation, value)
            
            # Add stop to gradient
            gradient.setColorAt(position, color)
    
    def _calculate_hue(self, position: float) -> float:
        """
        Calculate hue with sophisticated wave effects
        
        Args:
            position: Position along gradient (0.0-1.0)
            
        Returns:
            Hue value (0-360) with wave effects applied
        """
        # Primary wave - main color movement
        primary_hue = (self.animation_offset + position * 360) % 360
        
        # Secondary wave - rippling effect
        wave_effect = math.sin(
            (position * 2 * math.pi) + (self.wave_offset * math.pi / 180)
        ) * self.WAVE_AMPLITUDE_PRIMARY
        
        # Tertiary wave - shimmer effect
        shimmer_effect = math.sin(
            (position * 4 * math.pi) + (self.animation_offset * math.pi / 90)
        ) * self.WAVE_AMPLITUDE_SECONDARY
        
        # Combine all effects
        final_hue = (primary_hue + wave_effect + shimmer_effect) % 360
        
        return final_hue
    
    def _calculate_saturation(self, position: float) -> int:
        """
        Calculate saturation with professional range
        
        Args:
            position: Position along gradient (0.0-1.0)
            
        Returns:
            Saturation value (100-150) for professional appearance
        """
        base_saturation = 120
        variation = 30
        
        saturation = int(
            base_saturation + variation * math.sin(
                (position * math.pi) + (self.animation_offset * math.pi / 180)
            )
        )
        
        # Clamp to professional range
        return max(self.COLOR_SATURATION_RANGE[0], 
                  min(self.COLOR_SATURATION_RANGE[1], saturation))
    
    def _calculate_value(self, position: float) -> int:
        """
        Calculate brightness value with professional range
        
        Args:
            position: Position along gradient (0.0-1.0)
            
        Returns:
            Brightness value (160-200) for professional appearance
        """
        base_value = 180
        variation = 20
        
        value = int(
            base_value + variation * math.cos(
                (position * math.pi * 1.5) + (self.wave_offset * math.pi / 120)
            )
        )
        
        # Clamp to professional range
        return max(self.COLOR_VALUE_RANGE[0], 
                  min(self.COLOR_VALUE_RANGE[1], value))
