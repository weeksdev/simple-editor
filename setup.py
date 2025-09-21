#!/usr/bin/env python3
"""
Setup script for Simple Editor
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return "A simple, fast text editor for macOS, Ubuntu, and Windows"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), 'requirements.txt')
    if os.path.exists(requirements_path):
        with open(requirements_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]
    return []

setup(
    name="simple-editor",
    version="1.0.0",
    author="Simple Editor Team",
    author_email="",
    description="A simple, fast text editor similar to Windows Notepad",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/simple-editor",
    packages=find_packages(),
    py_modules=["simple_editor"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Editors",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    entry_points={
        "console_scripts": [
            "simple-editor=simple_editor_qt:main",
        ],
        "gui_scripts": [
            "simple-editor-gui=simple_editor_qt:main",
        ],
    },
    keywords="text editor notepad simple fast cross-platform",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/simple-editor/issues",
        "Source": "https://github.com/yourusername/simple-editor",
    },
)


