from typing import Any

from textual import on, events
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Input, Label, Button


class PasswordDialog(ModalScreen[str]):

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Enter the Password for the Database file:", id="pwd-dialog-label"),
            Input(placeholder="Password", password=True, id="pwd-dialog-input"),
            Button(label="Ok", variant="success", id="pwd-dialog-ok-btn"),
            id="pwd-dialog"
        )

    @on(Button.Pressed, "#pwd-dialog-ok-btn")
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
