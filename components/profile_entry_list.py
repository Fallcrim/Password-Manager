from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Static, ListView


class ProfileEntryList(Static):
    def compose(self) -> ComposeResult:
        yield Container(
            ListView(
                id="profile-entry-list"
            )
        )
