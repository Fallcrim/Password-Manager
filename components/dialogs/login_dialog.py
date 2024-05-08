from textual import on, events
from textual.app import ComposeResult
from textual.containers import Container
from textual.screen import ModalScreen
from textual.widgets import Button, Label, Input

from models import Profile


class LoginDialog(ModalScreen[Profile]):
    DEFAULT_CLASSES = "dialog"

    proceed = False

    def compose(self) -> ComposeResult:
        yield Container(
            Label("Username:", id="login-dialog-label-username", classes="dialog-label"),
            Input(placeholder="Username", id="login-dialog-input-username", classes="dialog-input"),

            Label("Password:", id="login-dialog-label-password", classes="dialog-label"),
            Input(placeholder="Password", id="login-dialog-input-password", classes="dialog-input"),

            Button("Login", "success", classes="dialog-ok-btn", id="login-dialog-save-btn"),

            id="login-dialog",
            classes="login-dialog-container"
        )

    @on(Button.Pressed, "#new-profile-dialog-save-btn")
    def handle_ok(self) -> None:
        self._pass_result()

    def _on_key(self, event: events.Key) -> None:
        if event.name == "enter":
            self._pass_result()

    def _pass_result(self) -> None:
        new_profile_data = tuple(r.value for r in self.query(Input).results())
        if len(new_profile_data) != 2:
            return

        self.dismiss(Profile(*new_profile_data))
