from typing import Iterator

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Label

from database import DatabaseManager
from config import load_config, save_config
from components.dialogs import PasswordDialog
from components.dialogs import OpenDatabaseDialog
from components.dialogs import ProfileEntryDialog
from components import ProfileEntryList
from models import Profile


class PasswordManagerGUI(App):
    CSS_PATH = "pm.tcss"
    BINDINGS = [
        ("ctrl+n", "new_entry", "New Entry"),
        ("ctrl+p", "command_palette", "Open Command Palette"),
        ("ctrl+s", "save_database", "Save File")
    ]
    TITLE = "Password Manager - by Fallcrim"

    config = load_config()
    profiles = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield ProfileEntryList()
        yield Footer()

    @work
    async def on_mount(self) -> None:
        if not self.config.get("database"):
            database_filename: str = await self.push_screen_wait(OpenDatabaseDialog())
            self.config["database"] = database_filename
        db_password = await self.push_screen_wait(PasswordDialog())
        self.notify("Loading profiles...")
        for profile in self.get_all_profiles():
            await self.async_append_profile(profile)
        self.notify("Profiles loaded.")

    async def action_new_entry(self) -> None:
        self.run_new_profile_dialog()

    @work
    async def run_new_profile_dialog(self) -> None:
        value = await self.push_screen_wait(ProfileEntryDialog())
        await self.async_append_profile(value)

    def action_quit(self) -> None:
        save_config(self.config)
        self.exit()

    def action_save_database(self) -> None:
        db = DatabaseManager(self.config.get("database"))
        for profile in self.profiles:
            db.insert_profile(profile.username, profile.application, profile.email, profile.password)
        self.notify("Profiles saved to " + self.config.get("database"))

    def get_all_profiles(self) -> Iterator[Profile]:
        if self.config.get("database"):
            db = DatabaseManager(self.config.get("database"))
            all_profiles = db.query_profiles("")
            for profile in all_profiles:
                yield Profile(*profile)

    async def async_append_profile(self, profile: Profile) -> None:
        await self.query_one("#profile-entry-list", ListView).append(
            ListItem(
                Label(
                    str(profile)
                )
            )
        )
        self.profiles.append(profile)
