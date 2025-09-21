#!/usr/bin/env python3
"""
Simple Text Editor - A fast, minimal text editor for macOS, Ubuntu, and Windows
Similar to Windows Notepad but with paste formatting stripped.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, font
import os
import sys
from tkinter.scrolledtext import ScrolledText


class SimpleEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple Editor")
        self.root.geometry("800x600")
        
        # Set window icon (if available)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # Current file path
        self.current_file = None
        self.is_modified = False
        
        # Create menu bar
        self.create_menu()
        
        # Create main text widget
        self.create_text_widget()
        
        # Bind events
        self.bind_events()
        
        # Configure window close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Set focus to text widget
        self.text_widget.focus_set()
    
    def create_menu(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New", command=self.new_file, accelerator="Cmd+N")
        file_menu.add_command(label="Open", command=self.open_file, accelerator="Cmd+O")
        file_menu.add_command(label="Save", command=self.save_file, accelerator="Cmd+S")
        file_menu.add_command(label="Save As", command=self.save_as_file, accelerator="Cmd+Shift+S")
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing, accelerator="Cmd+Q")
        
        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Undo", command=self.undo, accelerator="Cmd+Z")
        edit_menu.add_command(label="Redo", command=self.redo, accelerator="Cmd+Shift+Z")
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", command=self.cut, accelerator="Cmd+X")
        edit_menu.add_command(label="Copy", command=self.copy, accelerator="Cmd+C")
        edit_menu.add_command(label="Paste", command=self.paste_plain, accelerator="Cmd+V")
        edit_menu.add_separator()
        edit_menu.add_command(label="Select All", command=self.select_all, accelerator="Cmd+A")
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Zoom In", command=self.zoom_in, accelerator="Cmd+=")
        view_menu.add_command(label="Zoom Out", command=self.zoom_out, accelerator="Cmd+-")
        view_menu.add_command(label="Reset Zoom", command=self.reset_zoom, accelerator="Cmd+0")
    
    def create_text_widget(self):
        """Create the main text widget"""
        # Create frame for text widget
        text_frame = ttk.Frame(self.root)
        text_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # Create scrolled text widget
        self.text_widget = ScrolledText(
            text_frame,
            wrap=tk.WORD,
            undo=True,
            font=("Monaco", 12),  # Monaco is a good monospace font on macOS
            bg="white",
            fg="black",
            insertbackground="black",
            selectbackground="#007AFF",  # macOS blue selection color
            selectforeground="white"
        )
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # Configure text widget
        self.text_widget.config(tabs=("4c",))  # Set tab width to 4 characters
    
    def bind_events(self):
        """Bind keyboard and mouse events"""
        # Bind text modification events
        self.text_widget.bind("<<Modified>>", self.on_text_modified)
        
        # Bind keyboard shortcuts
        self.root.bind_all("<Command-n>", lambda e: self.new_file())
        self.root.bind_all("<Command-o>", lambda e: self.open_file())
        self.root.bind_all("<Command-s>", lambda e: self.save_file())
        self.root.bind_all("<Command-Shift-s>", lambda e: self.save_as_file())
        self.root.bind_all("<Command-q>", lambda e: self.on_closing())
        self.root.bind_all("<Command-z>", lambda e: self.undo())
        self.root.bind_all("<Command-Shift-z>", lambda e: self.redo())
        self.root.bind_all("<Command-x>", lambda e: self.cut())
        self.root.bind_all("<Command-c>", lambda e: self.copy())
        self.root.bind_all("<Command-v>", lambda e: self.paste_plain())
        self.root.bind_all("<Command-a>", lambda e: self.select_all())
        self.root.bind_all("<Command-=>", lambda e: self.zoom_in())
        self.root.bind_all("<Command-->", lambda e: self.zoom_out())
        self.root.bind_all("<Command-0>", lambda e: self.reset_zoom())
        
        # Bind paste event to strip formatting
        self.text_widget.bind("<Control-v>", lambda e: self.paste_plain())
        self.text_widget.bind("<Button-2>", lambda e: self.paste_plain())  # Middle mouse button
    
    def on_text_modified(self, event=None):
        """Handle text modification events"""
        if not self.is_modified:
            self.is_modified = True
            self.update_title()
    
    def update_title(self):
        """Update window title with file name and modification status"""
        if self.current_file:
            filename = os.path.basename(self.current_file)
            title = f"Simple Editor - {filename}"
        else:
            title = "Simple Editor - Untitled"
        
        if self.is_modified:
            title += " *"
        
        self.root.title(title)
    
    def new_file(self):
        """Create a new file"""
        if self.check_save():
            self.text_widget.delete(1.0, tk.END)
            self.current_file = None
            self.is_modified = False
            self.update_title()
    
    def open_file(self):
        """Open an existing file"""
        if self.check_save():
            file_path = filedialog.askopenfilename(
                title="Open File",
                filetypes=[
                    ("Text files", "*.txt"),
                    ("All files", "*.*")
                ]
            )
            
            if file_path:
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        content = file.read()
                    
                    self.text_widget.delete(1.0, tk.END)
                    self.text_widget.insert(1.0, content)
                    self.current_file = file_path
                    self.is_modified = False
                    self.update_title()
                    
                except Exception as e:
                    messagebox.showerror("Error", f"Could not open file:\n{str(e)}")
    
    def save_file(self):
        """Save the current file"""
        if self.current_file:
            try:
                content = self.text_widget.get(1.0, tk.END + "-1c")
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.is_modified = False
                self.update_title()
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
        else:
            self.save_as_file()
    
    def save_as_file(self):
        """Save the current file with a new name"""
        file_path = filedialog.asksaveasfilename(
            title="Save As",
            defaultextension=".txt",
            filetypes=[
                ("Text files", "*.txt"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            try:
                content = self.text_widget.get(1.0, tk.END + "-1c")
                with open(file_path, 'w', encoding='utf-8') as file:
                    file.write(content)
                
                self.current_file = file_path
                self.is_modified = False
                self.update_title()
                
            except Exception as e:
                messagebox.showerror("Error", f"Could not save file:\n{str(e)}")
    
    def check_save(self):
        """Check if file needs to be saved before proceeding"""
        if self.is_modified:
            result = messagebox.askyesnocancel(
                "Save Changes",
                "The file has been modified. Do you want to save changes?"
            )
            
            if result is True:
                self.save_file()
                return True
            elif result is False:
                return True
            else:
                return False
        
        return True
    
    def undo(self):
        """Undo last action"""
        try:
            self.text_widget.edit_undo()
        except tk.TclError:
            pass
    
    def redo(self):
        """Redo last undone action"""
        try:
            self.text_widget.edit_redo()
        except tk.TclError:
            pass
    
    def cut(self):
        """Cut selected text"""
        try:
            self.text_widget.event_generate("<<Cut>>")
        except tk.TclError:
            pass
    
    def copy(self):
        """Copy selected text"""
        try:
            self.text_widget.event_generate("<<Copy>>")
        except tk.TclError:
            pass
    
    def paste_plain(self):
        """Paste text without formatting"""
        try:
            # Get clipboard content
            clipboard_content = self.root.clipboard_get()
            
            # Insert plain text at current cursor position
            self.text_widget.insert(tk.INSERT, clipboard_content)
            
        except tk.TclError:
            # If clipboard is empty or contains non-text data, do nothing
            pass
    
    def select_all(self):
        """Select all text"""
        self.text_widget.tag_add(tk.SEL, "1.0", tk.END)
        self.text_widget.mark_set(tk.INSERT, "1.0")
        self.text_widget.see(tk.INSERT)
    
    def zoom_in(self):
        """Increase font size"""
        current_font = font.Font(font=self.text_widget['font'])
        size = current_font['size']
        if size < 72:  # Maximum font size
            self.text_widget.config(font=(current_font['family'], size + 2))
    
    def zoom_out(self):
        """Decrease font size"""
        current_font = font.Font(font=self.text_widget['font'])
        size = current_font['size']
        if size > 6:  # Minimum font size
            self.text_widget.config(font=(current_font['family'], size - 2))
    
    def reset_zoom(self):
        """Reset font size to default"""
        self.text_widget.config(font=("Monaco", 12))
    
    def on_closing(self):
        """Handle window closing"""
        if self.check_save():
            self.root.quit()
            self.root.destroy()


def main():
    """Main function to run the application"""
    root = tk.Tk()
    
    # Configure for macOS
    if sys.platform == "darwin":
        # Set appearance for macOS
        root.tk.call("tk", "scaling", 2.0)  # High DPI scaling
    
    app = SimpleEditor(root)
    root.mainloop()


if __name__ == "__main__":
    main()


