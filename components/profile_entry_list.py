from textual import on
from textual.app import ComposeResult
from textual.containers import ScrollableContainer
from textual.message import Message
from textual.widgets import Static, ListView


class ProfileEntryList(Static):
    class ProfileList(ListView):
        confirm_selection = False
        selected_item = None

        @on(ListView.Selected)
        def handle_item_selected(self, event: ListView.Selected):
            if event.item != self.selected_item:
                self.selected_item = event.item
                self.confirm_selection = False
            elif not self.confirm_selection:
                self.selected_item = event.item
                self.confirm_selection = True
                return

            self.notify("Item selected!")
            self.confirm_selection = False

    def compose(self) -> ComposeResult:
        yield ScrollableContainer(
            self.ProfileList(
                id="profile-entry-list",
            )
        )
