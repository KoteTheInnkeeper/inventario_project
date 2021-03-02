import sqlite3
import logging

from databases.database_connection import DatabaseCursor
from werkzeug.security import generate_password_hash, check_password_hash

from typing import Tuple, Union

# Error handling
from utils.errors import UnmatchedUsername, UnmatchedPassword, UserNotUnique
from sqlite3.dbapi2 import OperationalError, IntegrityError

# Set the logger
log = logging.getLogger('inventory_logger.login_management')


class UserDatabase:
    """
    A class for managing the users and operate with them (signing them up, signing them out, checking if
    the login info is correct, etc.)
    """
    def __init__(self, host: str):
        self.host = host

        log.debug(f"Looking for the '{self.host}' file.")
        try:
            with open(self.host, 'r'):
                log.debug(f"The file '{self.host}' exists.")
        except FileNotFoundError:
            log.error(f"The file '{self.host}' doesn't exists. Creating one.")
            with open(self.host, 'w'):
                log.debug("File created succesfully.")

        log.debug(f"Checking the integrity of {self.host}.")
        log.debug("Creating a 'users' table if it doesn't exists already")
        try:
            with DatabaseCursor(self.host) as cursor:
                cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE primary key, password TEXT)")
        except OperationalError:
            log.critical("An OperationalError was raised by sqlite3.")
            raise
        else:
            log.debug("The database is ready to be used.")

    def check_if_users(self):
        """This method allows to know if there are any users at all registered. This can be useful in systems
        where we want only to be an unique user.
        :return: False if there are no users at all. True if there are.
        """
        try:
            with DatabaseCursor(self.host) as cursor:
                log.debug("Checking if there are users registered.")
                cursor.execute("SELECT username FROM users")
                results = cursor.fetchall()
                if results:
                    log.debug("There are users")
                    return True
                else:
                    log.error("There aren't any users at all.")
                    return False
        except OperationalError:
            log.critical("An OperationalError was raised by sqlite3.")


    def new_user(self, username: str, hashed_password: str) -> bool:
        """A method used for creating a new user.
        :param username: the username. Must be unique.
        :param hashed_password: The password already hashed.
        :return: For now, Booleans. True if the user was added. False or None if it didn't.
        """
        username = username.lower()
        log.debug("Adding a new user.")
        try:
            with DatabaseCursor(self.host) as cursor:
                log.debug("Adding the new user.")
                try:
                    cursor.execute("INSERT INTO users VALUES(?, ?)", (username, hashed_password))
                except IntegrityError:
                    raise UserNotUnique('The provided username is already in use.')
                else:
                    log.debug(f"The user {username} was registered correctly!")
                    return True
        except OperationalError:
            log.critical("An OperationalError was raised by sqlite3")
            raise
        except UserNotUnique:
            log.critical("There was a match in usernames. They must be unique.")
            return False

    def check_login(self, username: str, password: str) -> Tuple[bool, bool]:
        """Checks if the provided login info matches what's stored in the database.
        :param username: username provided
        :param password: password provided
        :return: A tuple where the first element stands for the truthfulness of a username match and the
        second one does it for a password match.
        """
        username = username.lower()
        try:
            with DatabaseCursor(self.host) as cursor:
                cursor.execute("SELECT password FROM users where username=?", (username, ))
                result = cursor.fetchone()
                if not result:
                    raise UnmatchedUsername('No match for such username')
                hashed_password = result[0]
                if check_password_hash(hashed_password, password):
                    return True, True
                else:
                    raise UnmatchedPassword('There was a username match, but not a password one.')
        except UnmatchedUsername:
            log.error("There wasn't a match for such username.")
            return False, False
        except UnmatchedPassword:
            log.error("The wasn't a match for such password, altough the username was right.")
            return True, False



