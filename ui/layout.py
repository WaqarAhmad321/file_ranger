from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table

console = Console()

class FileManagerUI:

    def __init__(self):
        self.layout = Layout()
        self.current_path = "/"
        self.folders = ["home", "documents", "downloads", "music", "pictures"]
        self.files = ["file1.txt", "file2.pdf", "image.png"]

        self.selected_index = 0

    def build_layout(self):
        self.layout.split(
            Layout(name="header", size=3),
            Layout(name="body", ratio=1),
            Layout(name="footer", size=3)
        )

        self.layout["body"].split_row(
            Layout(name="sidebar", size=30),
            Layout(name="main", ratio=1)
        )

    def render_header(self):
        return Panel(f" TUI File Manager ", style="bold blue")

    def render_sidebar(self):
        table = Table(show_header=False, expand=True)
        for folder in self.folders:
            table.add_row(folder)
        return Panel(table, title="Folders", border_style="cyan")

    def render_main(self):
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Name", justify="left")
        table.add_column("Type", justify="center")

        for i, file in enumerate(self.files):
            style = "reverse" if i == self.selected_index else ""
            table.add_row(file, "File", style=style)

        return Panel(table, title=f"Path: {self.current_path}", border_style="green")

    def render_footer(self):
        return Panel(
            "[b]↑/↓[/b] Move   [b]Enter[/b] Open   [b]Q[/b] Quit",
            border_style="yellow"
        )

    def render(self):
        self.layout["header"].update(self.render_header())
        self.layout["sidebar"].update(self.render_sidebar())
        self.layout["main"].update(self.render_main())
        self.layout["footer"].update(self.render_footer())

        console.clear()
        console.print(self.layout)

    def move_selection(self, direction):
        if direction == "up":
            self.selected_index = max(0, self.selected_index - 1)
        else:
            self.selected_index = min(len(self.files)-1, self.selected_index + 1)
