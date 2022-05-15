"""
This module is created to implement the SQLite database.

It creates the required user.db tables and takes care connection.
"""
import sqlite3
from logging import info


class DB:
    """SQLite database implementation"""
    sqlite_file = 'users.db'
    connection = None

    def __init__(self):
        """Initialise the database"""
        info('Initialising the database')
        self.connect_to_db()

    @staticmethod
    def connect_to_db():
        """Create the connection and create tables in the users.db"""

        info('Connecting to database')

        if DB.connection is not None:
            info('Database has already been opened')
            return

        # Connecting to the database file
        DB.connection = sqlite3.connect(DB.sqlite_file, check_same_thread=False)
        cursor = DB.connection.cursor()

        # create a new table and commit
        info('Creating tables in the database')
        cursor.execute('CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, date_of_birth TEXT NOT NULL)')
        DB.connection.commit()

        # ensure the synchronous disk write for the database
        cursor.execute('PRAGMA synchronous=FULL')

    def close_connection(self):
        """Close db connection"""

        if DB.connection is not None:
            info('Closing the connection')
            self.close_db_connection()

    @staticmethod
    def close_db_connection():
        """Commit and close the connection"""

        DB.connection.commit()
        DB.connection.close()
