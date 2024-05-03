from dataclasses import dataclass


@dataclass
class Profile:
    username: str
    application: str
    email: str
    password: str
    notes: str

    def __str__(self):
        return f"{self.application} - {self.username}"
