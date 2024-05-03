import sqlite3
from sqlite3 import Connection

from encryption import EncryptionHandler


class DatabaseManager(object):
    def __init__(self, file_path: str, database_password: str):
        self._file_path = file_path
        self._database_password = database_password
        self._connection = self._connect()
        self._create_tables()

    def _connect(self) -> Connection:
        """
        First encrypts and then returns an SQLite3 Connection object
        :return:
        """
        encryption_handler: EncryptionHandler = EncryptionHandler(self._database_password.encode())
        with open(self._file_path, "rb") as in_file:
            enc_data: bytes = encryption_handler.decrypt(in_file.read())
        with open(self._file_path, "wb") as outfile:
            outfile.write(enc_data)
        return sqlite3.connect(self._file_path)

    def _create_tables(self) -> None:
        """
        Creates the initial table required if the table is not already present
        :return:
        """
        with self._connection.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS 'profiles' (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, application TEXT, email TEXT, password TEXT, notes TEXT);")
            self._connection.commit()

    def insert_profile(self, username: str, application: str, email: str, password: str, notes: str) -> None:
        """
        Inserts a new profile into the database, which contains account information the user wants to store
        :param username:
        :param application:
        :param email:
        :param password:
        :param notes:
        :return:
        """
        with self._connection.cursor() as cursor:
            cursor.execute("INSERT INTO 'profiles' (username, application, email, password, notes) VALUES (?, ?, ?, ?);", (username, application, email, password, notes))
            self._connection.commit()

    def get_profile(self, query: str) -> tuple | None:
        """
        Fetches alle profiles, which have the query either in their username, application or email field
        :param query:
        :return:
        """
        with self._connection.cursor() as cursor:
            cursor.execute("SELECT (username, application, email, password, notes) FROM 'profiles' WHERE 'username' LIKE '%?%' OR 'application' LIKE '%?%' OR 'email' LIKE '%?%';", (query, query, query,))
            return cursor.fetchall()

    def _close_connection(self):
        """
        Closes the database connection and encrypts the db file
        :return:
        """
        self._connection.close()
        self._encrypt_database()

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
