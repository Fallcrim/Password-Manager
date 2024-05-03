from textual import on, events
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input, TextArea

from models import Profile


class CreateNewProfileDialog(ModalScreen[Profile]):
    DEFAULT_CLASSES = "dialog"

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            Label("Username:", id="new-profile-dialog-label", classes="dialog-label"),
            Input(placeholder="e.g. SwiftiesSuck42", id="new-profile-dialog-input", classes="dialog-input"),
            Label("Application:", id="new-profile-dialog-label", classes="dialog-label"),
            Input(placeholder="e.g. Instagram", id="new-profile-dialog-input", classes="dialog-input"),
            Label("Email:", id="new-profile-dialog-label", classes="dialog-label"),
            Input(placeholder="e.g. limpbiscuit@outlookie.com", id="new-profile-dialog-input", classes="dialog-input"),
            Label("Password:", id="new-profile-dialog-label", classes="dialog-label"),
            Input(id="new-profile-dialog-input", classes="dialog-input"),
            Label("Notes:", id="new-profile-dialog-label", classes="dialog-label"),
            TextArea(tab_behavior="indent", show_line_numbers=True, id="new-profile-dialog-input", classes="dialog-input"),
            Button("Save", "success", classes="dialog-ok-btn", id="new-profile-dialog-save-btn"),
            id="new-profile-dialog",
            classes="new-profile-dialog-container"
        )

    @on(Button.Pressed, "#new-profile-dialog-save-btn")
    def handle_ok(self) -> None:
        self.pass_result()

    def _on_key(self, event: events.Key) -> None:
        if event.name == "enter":
            self.pass_result()

    def pass_result(self) -> None:
        new_profile_data = (r.value for r in self.query(Input).results())
        if not new_profile_data:
            return

        self.dismiss(Profile(*new_profile_data))
