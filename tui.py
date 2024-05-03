from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from database import DatabaseManager
from config import load_config
from components.password_dialog import PasswordDialog


class PasswordManagerGUI(App):
    CSS_PATH = "pm.tcss"
    BINDINGS = [
        ("ctrl+n", "new_entry", "New Entry"),
        ("ctrl+p", "command_palette", "Open Command Palette"),
    ]
    CONFIG = load_config()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, name="Password Manager - by Fallcrim")
        yield Footer()

    @work
    async def on_mount(self) -> None:
        tst = await self.push_screen_wait(PasswordDialog())
        self.notify(tst)

    def action_new_entry(self) -> None:
        pass

    def get_all_profiles(self):
        if self.CONFIG.get("database"):
            db = DatabaseManager(self.CONFIG.get("database"))
            all_profiles = db.get_profile("*")
