from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Input, Label
from textual.containers import Vertical, Center

class InputModal(ModalScreen[str]):
    """A modal screen for getting user input."""

    CSS = """
    InputModal {
        align: center middle;
    }

    #dialog {
        padding: 1 2;
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
    }

    Label {
        margin-bottom: 1;
        width: 100%;
        text-align: center;
    }

    Input {
        width: 100%;
    }
    """

    def __init__(self, prompt: str, initial_value: str = ""):
        super().__init__()
        self.prompt = prompt
        self.initial_value = initial_value

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(self.prompt)
            yield Input(value=self.initial_value, id="input")

    def on_mount(self) -> None:
        self.query_one(Input).focus()

    def on_input_submitted(self, event: Input.Submitted) -> None:
        self.dismiss(event.value)
