from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header

from database import DatabaseManager
from config import load_config
from components.dialogs import PasswordDialog
from components.dialogs import OpenDatabaseDialog


class PasswordManagerGUI(App):
    CSS_PATH = "pm.tcss"
    BINDINGS = [
        ("ctrl-n", "new_entry", "New Entry"),
        ("ctrl-p", "command_palette", "Open Command Palette"),
    ]
    CONFIG = load_config()

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True, name="Password Manager - by Fallcrim")
        yield Footer()

    @work
    async def on_mount(self) -> None:
        database_filename: str = await self.push_screen_wait(OpenDatabaseDialog())
        self.CONFIG["database"] = database_filename
        db_password = await self.push_screen_wait(PasswordDialog())
        self.get_all_profiles(db_password)

    def action_new_entry(self) -> None:
        pass

    def get_all_profiles(self, db_password: str):
        if self.CONFIG.get("database"):
            db = DatabaseManager(self.CONFIG.get("database"), db_password)
            all_profiles = db.get_profile("*")
