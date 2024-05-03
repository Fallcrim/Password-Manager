from textual import on, events
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.validation import Function
from textual.widgets import Button, Label, Input


class OpenDatabaseDialog(ModalScreen[str]):
    DEFAULT_CLASSES = "dialog"

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Enter the absolute path for the Database file:", id="db-dialog-label", classes="dialog-label"),
            Input(
                placeholder="e.g. /usr/local/share/passwords.pstore",
                id="db-dialog-input",
                classes="dialog-input",
                validators=[
                    Function(validate_filename, "File does not end with .pstore")
                ]
            ),
            Button(label="Ok", variant="success", id="db-dialog-ok-btn", classes="dialog-ok-btn"),
            id="db-dialog",
            classes="dialog-container"
        )

    @on(Button.Pressed, "#db-dialog-ok-btn")
    def handle_ok(self) -> None:
        self.pass_result()

    def _on_key(self, event: events.Key) -> None:
        if event.name == "enter":
            self.pass_result()

    def pass_result(self) -> None:
        result = self.query_one(Input).value
        if not result:
            return
        self.dismiss(result)


def validate_filename(value: str) -> bool:
    return value.endswith(".pstore")
