import os
import sys
from pathlib import Path
from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static, OptionList
from textual.widgets.option_list import Option
from textual.reactive import reactive
from rich.text import Text
from rich.syntax import Syntax
from input_modal import InputModal
from icons import get_icon

# Try to import the C++ backend
try:
    import backend
except ImportError:
    print("❌ Error: 'backend' module not found.")
    print("   Make sure compiled the C++ code and copied the .so file to this directory.")
    sys.exit(1)

class StatusBar(Static):
    """A custom status bar widget."""
    
    def compose(self) -> ComposeResult:
        yield Static(id="status-path")
        yield Static(id="status-info")

    def update_status(self, path: str, info: str):
        self.query_one("#status-path").update(f" {path}")
        self.query_one("#status-info").update(f"{info} ")

class FileManagerApp(App):
    CSS = """
    Screen {
        layout: vertical;
        background: #151515;
    }

    /* Layout for the 3 panes */
    #main-container {
        height: 1fr;
        background: #151515;
    }

    /* Left Pane (Parent) */
    #left-pane {
        width: 20%;
        height: 100%;
        background: #1e1e1e;
        border-right: solid #333;
        color: #666;
    }

    /* Middle Pane (Current) */
    #middle-pane {
        width: 50%;
        height: 100%;
        background: #262626;
        border-right: solid #333;
    }

    /* Right Pane (Preview) */
    #right-pane {
        width: 30%;
        height: 100%;
        background: #1e1e1e;
        padding: 0 1;
    }

    /* OptionList Styling */
    OptionList {
        background: #3e3e3e;
        border: none;
        scrollbar-gutter: stable;
        color: #000;
    }
    
    OptionList:focus {
        border: none;
    }

    /* Remove the default highlight to use our custom one */
    .option-list--highlighted {
        background: #3e3e3e;
        color: white;
        text-style: bold;
    }

    /* Status Bar */
    StatusBar {
        dock: top;
        height: 1;
        background: #007acc;
        color: white;
        layout: horizontal;
    }

    #status-path {
        width: 70%;
        content-align: left middle;
    }

    #status-info {
        width: 30%;
        content-align: right middle;
    }
    
    /* Preview Title */
    #preview-title {
        background: #333;
        color: white;
        padding: 0 1;
        text-style: bold;
        margin-bottom: 1;
    }
    """

    BINDINGS = [
        ("q", "quit", "Quit"),
        ("j", "cursor_down", "Down"),
        ("k", "cursor_up", "Up"),
        ("l", "select_item", "Enter"),
        ("h", "go_back", "Back"),
        ("enter", "select_item", "Enter"),
        ("left", "go_back", "Back"),   # Added Left Arrow
        ("right", "select_item", "Enter"), # Added Right Arrow
        ("L", "go_forward", "Forward"), # Shift+Right or L
        ("d", "delete_item", "Delete"),
        ("r", "rename_item", "Rename"),
        ("n", "new_file", "New File"),
        ("N", "new_directory", "New Folder"),
        ("c", "copy_item", "Copy"),
        ("p", "paste_item", "Paste"),
    ]

    # Reactive state for current path
    current_path = reactive(os.getcwd())
    
    # Track the folder we just exited to highlight it in the parent view
    last_exited_path = None
    
    # Clipboard for copy/paste
    clipboard_path = None

    def compose(self) -> ComposeResult:
        """Create the 3-pane layout."""
        yield StatusBar()
        with Horizontal(id="main-container"):
            yield OptionList(id="left-pane", disabled=True)
            yield OptionList(id="middle-pane")
            with Vertical(id="right-pane"):
                yield Static(id="preview-title", content="")
                yield Static(id="preview-content", expand=True)
        yield Footer()

    def on_mount(self) -> None:
        """Initialize the app."""
        self.title = "DSA File Manager"
        # Initialize C++ History Manager
        self.history = backend.HistoryManager()
        self.history.init(self.current_path)
        self.refresh_ui()
        self.query_one("#middle-pane").focus()

    def watch_current_path(self, old_path: str, new_path: str) -> None:
        self.refresh_ui()

    def get_directory_contents(self, path: str):
        """Helper to get sorted contents using C++ backend"""
        try:
            node = backend.list_directory(path)
            # Backend now returns sorted children (directories first, case-insensitive)
            return node.children
        except Exception as e:
            return []

    def format_option(self, node, is_selected=False) -> Text:
        """Format a file option with icon and color."""
        icon = get_icon(node.name, node.is_directory)
        
        if node.is_directory:
            style = "bold blue" if is_selected else "blue"
        else:
            style = "white"
            
        text = Text(f"{icon} {node.name}", style=style)
        return text

    def refresh_ui(self):
        path_obj = Path(self.current_path)
        
        # Update Status Bar
        try:
            current_contents = self.get_directory_contents(self.current_path)
            item_count = len(current_contents)
            self.query_one(StatusBar).update_status(self.current_path, f"{item_count} items")
        except:
            self.query_one(StatusBar).update_status(self.current_path, "Error")
            current_contents = []

        # 1. Update Left Pane (Parent)
        left_list = self.query_one("#left-pane", OptionList)
        left_list.clear_options()
        
        parent_path = path_obj.parent
        if parent_path != path_obj: # If not root
            try:
                parent_contents = self.get_directory_contents(str(parent_path))
                for node in parent_contents:
                    left_list.add_option(Option(self.format_option(node), id=node.path))
                    # Highlight the folder we are currently inside
                    if node.name == path_obj.name:
                        left_list.highlighted = left_list.option_count - 1
            except:
                pass

        # 2. Update Middle Pane (Current)
        middle_list = self.query_one("#middle-pane", OptionList)
        middle_list.clear_options()
        
        self.current_contents_map = {} # Map index to node for easy access
        
        highlight_index = 0 # Default to top
        
        for idx, node in enumerate(current_contents):
            middle_list.add_option(Option(self.format_option(node), id=node.path))
            self.current_contents_map[idx] = node
            
            # If we just came back from a subdirectory, highlight it
            if self.last_exited_path and node.path == self.last_exited_path:
                highlight_index = idx

        # Reset last exited path
        self.last_exited_path = None

        # Set highlight
        if current_contents:
            middle_list.highlighted = highlight_index
            self.update_preview(current_contents[highlight_index])
        else:
            self.query_one("#preview-content", Static).update("Empty directory")
            self.query_one("#preview-title", Static).update("")

    def on_option_list_option_highlighted(self, event: OptionList.OptionHighlighted) -> None:
        """When selection changes in the middle pane, update preview"""
        if event.option_list.id == "middle-pane":
            if event.option_index is not None and event.option_index in self.current_contents_map:
                node = self.current_contents_map[event.option_index]
                self.update_preview(node)

    def update_preview(self, node):
        title = self.query_one("#preview-title", Static)
        content = self.query_one("#preview-content", Static)
        
        title.update(Text(f"Preview: {node.name}", style="bold yellow"))

        if node.is_directory:
            # Directory Summary
            try:
                sub_contents = self.get_directory_contents(node.path)
                summary = f"\n[bold]Directory Content:[/]\n\n"
                for i, child in enumerate(sub_contents[:15]): # Show first 15
                    icon = "📂" if child.is_directory else "📄"
                    summary += f"{icon} {child.name}\n"
                if len(sub_contents) > 15:
                    summary += f"\n... and {len(sub_contents) - 15} more items."
                content.update(summary)
            except:
                content.update("Access Denied")
        else:
            # File Preview
            try:
                file_path = Path(node.path)
                if file_path.suffix.lower() in ['.txt', '.py', '.cpp', '.h', '.md', '.json', '.yml', '.cmake']:
                    with open(file_path, "r", encoding="utf-8") as f:
                        text = f.read(2000) # Read first 2000 chars
                    
                    # Simple syntax highlighting for code
                    if file_path.suffix in ['.py', '.cpp', '.h']:
                        lexer = "python" if file_path.suffix == '.py' else "cpp"
                        syntax = Syntax(text, lexer, theme="monokai", line_numbers=True)
                        content.update(syntax)
                    else:
                        content.update(text)
                else:
                    content.update(f"\n[italic]Binary file or unknown format.\nSize: {node.size} bytes[/]")
            except Exception as e:
                content.update(f"Error reading file: {e}")

    def action_cursor_down(self):
        self.query_one("#middle-pane").action_cursor_down()

    def action_cursor_up(self):
        self.query_one("#middle-pane").action_cursor_up()

    def action_select_item(self):
        middle_list = self.query_one("#middle-pane", OptionList)
        idx = middle_list.highlighted
        
        if idx is not None and idx in self.current_contents_map:
            node = self.current_contents_map[idx]
            if node.is_directory:
                # Push to C++ History
                self.history.push(node.path)
                self.current_path = node.path
            else:
                # For now, just notify. Later: Open file
                self.notify(f"Selected file: {node.name}")

    def action_go_back(self):
        # Use C++ History
        prev_path = self.history.go_back()
        if prev_path:
            self.last_exited_path = self.current_path
            self.current_path = prev_path

    def action_go_forward(self):
        # Use C++ History
        next_path = self.history.go_forward()
        if next_path:
            self.current_path = next_path

    def action_copy_item(self):
        node = self.get_selected_node()
        if node:
            self.clipboard_path = node.path
            self.notify(f"Copied to clipboard: {node.name}")

    def action_paste_item(self):
        if not self.clipboard_path:
            self.notify("Clipboard is empty", severity="warning")
            return

        src = Path(self.clipboard_path)
        dest = Path(self.current_path) / src.name
        
        if backend.copy_path(str(src), str(dest)):
            self.notify(f"Pasted: {src.name}")
            self.refresh_ui()
        else:
            self.notify(f"Failed to paste: {src.name}", severity="error")

    def get_selected_node(self):
        middle_list = self.query_one("#middle-pane", OptionList)
        idx = middle_list.highlighted
        if idx is not None and idx in self.current_contents_map:
            return self.current_contents_map[idx]
        return None

    def action_delete_item(self):
        node = self.get_selected_node()
        if not node:
            return

        def check_confirm(confirm_str: str):
            if confirm_str.lower() == "y":
                if backend.remove_path_recursive(node.path):
                    self.notify(f"Deleted: {node.name}")
                    self.refresh_ui()
                else:
                    self.notify(f"Failed to delete: {node.name}", severity="error")

        self.push_screen(InputModal(f"Delete '{node.name}'? (y/n)"), check_confirm)

    def action_rename_item(self):
        node = self.get_selected_node()
        if not node:
            return

        def do_rename(new_name: str):
            if not new_name or new_name == node.name:
                return
            
            new_path = str(Path(node.path).parent / new_name)
            if backend.rename_path(node.path, new_path):
                self.notify(f"Renamed to: {new_name}")
                self.refresh_ui()
            else:
                self.notify(f"Failed to rename to: {new_name}", severity="error")

        self.push_screen(InputModal(f"Rename '{node.name}' to:", node.name), do_rename)

    def action_new_file(self):
        def do_create_file(name: str):
            if not name:
                return
            new_path = str(Path(self.current_path) / name)
            if backend.touch_file(new_path):
                self.notify(f"Created file: {name}")
                self.refresh_ui()
            else:
                self.notify(f"Failed to create file: {name}", severity="error")

        self.push_screen(InputModal("New File Name:"), do_create_file)

    def action_new_directory(self):
        def do_create_dir(name: str):
            if not name:
                return
            new_path = str(Path(self.current_path) / name)
            if backend.make_directory_recursive(new_path):
                self.notify(f"Created folder: {name}")
                self.refresh_ui()
            else:
                self.notify(f"Failed to create folder: {name}", severity="error")

        self.push_screen(InputModal("New Folder Name:"), do_create_dir)

if __name__ == "__main__":
    app = FileManagerApp()
    app.run()