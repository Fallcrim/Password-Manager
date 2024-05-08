import sqlite3
from sqlite3 import Connection
from typing import List, Tuple

import supabase_auth

from encryption import EncryptionHandler


class DatabaseManager(object):
    def __init__(self, file_path: str, config: dict):
        self._file_path = file_path
        self.app_config = config
        # self._database_password = database_password
        self.connection = supabase_auth.SyncGoTrueClient(url="")
        self._create_tables()

    def _connect(self) -> Connection:
        """
        First encrypts and then returns an SQLite3 Connection object
        :return:
        """
        # encryption_handler: EncryptionHandler = EncryptionHandler(self._database_password.encode())
        # with open(self._file_path, "rb") as in_file:
        #     enc_data: bytes = encryption_handler.decrypt(in_file.read())
        # with open(self._file_path, "wb") as outfile:
        #     outfile.write(enc_data)
        return sqlite3.connect(self._file_path)

    def _create_tables(self) -> None:
        """
        Creates the initial table required if the table is not already present
        :return:
        """
        cursor = self._connection.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS 'profiles' (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, application TEXT, email TEXT, password TEXT);")
        self._connection.commit()
        cursor.close()

    def insert_profile(self, username: str, application: str, email: str, password: str) -> None:
        """
        Inserts a new profile into the database, which contains account information the user wants to store
        :param username:
        :param application:
        :param email:
        :param password:
        :return:
        """
        cursor = self._connection.cursor()
        cursor.execute("INSERT INTO 'profiles' (username, application, email, password) VALUES (?, ?, ?, ?);", (username, application, email, password))
        self._connection.commit()
        cursor.close()

    def query_profiles(self, query: str) -> List[Tuple[str, str, str, str]]:
        """
        Fetches all profiles, which have the query either in their username, application or email field
        :param query:
        :return:
        """
        cursor = self._connection.cursor()
        cursor.execute(f"SELECT username, application, email, password FROM 'profiles' WHERE username LIKE '%{query}%';")
        result = cursor.fetchall()
        cursor.close()
        return result

    def _close_connection(self):
        """
        Closes the database connection and encrypts the db file
        :return:
        """
        self._connection.close()
        # self._encrypt_database()

    def _encrypt_database(self):
        """
        Encrypts the database file
        :return:
        """
        encryption_handler: EncryptionHandler = EncryptionHandler(self._database_password.encode())
        with open(self._file_path, "rb") as in_file:
            enc_data: bytes = encryption_handler.encrypt(in_file.read())
        with open(self._file_path, "wb") as outfile:
            outfile.write(enc_data)

    def __del__(self):
        self._close_connection()
