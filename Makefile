# Makefile for Simple Editor

.PHONY: install test run clean help

# Default target
help:
	@echo "Simple Editor - Available targets:"
	@echo "  install  - Install the editor via pip"
	@echo "  test     - Run tests"
	@echo "  run      - Run the editor"
	@echo "  clean    - Clean up temporary files"
	@echo "  help     - Show this help message"

# Install the editor
install:
	@echo "Installing Simple Editor..."
	pip3 install .

# Run tests
test:
	@echo "Running tests..."
	python3 test_editor.py

# Run the editor
run:
	@echo "Starting Simple Editor..."
	python3 simple_editor.py

# Clean up
clean:
	@echo "Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

# Development installation
dev-install:
	@echo "Installing in development mode..."
	pip3 install -e .


