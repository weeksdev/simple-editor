#!/usr/bin/env python3
"""
Simple Editor - Enterprise Entry Point

This is the main entry point for the Simple Editor application using
the enterprise-level refactored codebase.

Features:
- Professional code organization with proper abstractions
- Comprehensive documentation and type hints
- Enterprise-level error handling and logging
- Cross-platform compatibility
- Memory-efficient design patterns
"""

import sys
import os

# Add src directory to Python path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.main import main

if __name__ == "__main__":
    sys.exit(main())
