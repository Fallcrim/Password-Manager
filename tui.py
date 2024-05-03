from typing import Iterator

from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, ListView, ListItem, Label

from database import DatabaseManager
from config import load_config, save_config
from components.dialogs import PasswordDialog
from components.dialogs import OpenDatabaseDialog
from components.dialogs import CreateNewProfileDialog
from models import Profile


class PasswordManagerGUI(App):
    CSS_PATH = "pm.tcss"
    BINDINGS = [
        ("ctrl-n", "new_entry", "New Entry"),
        ("ctrl-p", "command_palette", "Open Command Palette"),
    ]
    TITLE = "Password Manager - by Fallcrim"

    config = load_config()
    profiles = []

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()

    @work
    async def on_mount(self) -> None:
        database_filename: str = await self.push_screen_wait(OpenDatabaseDialog())
        self.config["database"] = database_filename
        db_password = await self.push_screen_wait(PasswordDialog())
        self.notify("Loading profiles...")
        for profile in self.get_all_profiles(db_password):
            await self.async_append_profile(profile)
        self.notify("Profiles loaded.")

    def action_new_entry(self) -> None:
        new_profile = self.push_screen(CreateNewProfileDialog(), wait_for_dismiss=True).result()
        self.append_profile(new_profile)

    def action_quit(self) -> None:
        save_config(self.config)
        self.exit()

    def get_all_profiles(self, db_password: str) -> Iterator[Profile]:
        if self.config.get("database"):
            db = DatabaseManager(self.config.get("database"), db_password)
            all_profiles = db.query_profiles("*")
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

    async def append_profile(self, profile: Profile) -> None:
        self.query("#profile-entry-list").first().append(
            ListItem(
                Label(
                    str(profile)
                )
            )
        )
        self.profiles.append(profile)
