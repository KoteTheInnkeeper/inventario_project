import logging

from databases.database_connection import DatabaseCursor
from werkzeug.security import check_password_hash

# Typing
from typing import List
# Error handling
from utils.errors import DatabaseInitError, ProductExists, UnableToAdd
from _sqlite3 import OperationalError, InternalError, IntegrityError

# Set the basic configurations for the logger
logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s", level=logging.DEBUG,
                    filename='log.txt')
# Create the logger
log = logging.getLogger("inventory_logger.database_management")


class Database:
    """
        A class to manage all of the .db file as a database with methods.
    """
    def __init__(self, host: str):
        self.host = host
        # Checking for the file and creating it if it isn' there.
        try:
            log.debug(f"Checking if the file {self.host} exists at all.")
            with open(self.host, 'r'):
                log.debug(f"{self.host} exists.")
        except FileNotFoundError:
            log.critical(f"The file {self.host} doesn't exists. Creating a new one.")
            with open(self.host, 'w'):
                log.critical(f"Created the {self.host} file.")

        # Now we can start initializing the database.
        try:
            with DatabaseCursor(self.host) as cursor:
                log.debug("Creating 'products' table if it doesn't exists already.")
                cursor.execute("CREATE TABLE IF NOT EXISTS products(name TEXT UNIQUE primary key, cost_price REAL, "
                               "sell_price REAL, in_stock INTEGER)")
                log.debug("Creating the 'users' table if it doesn't exists already")
                cursor.execute("CREATE TABLE IF NOT EXISTS users(username TEXT UNIQUE primary key, password TEXT)")
        except Exception:
            log.critical("Unable to initialize the database.")
            raise DatabaseInitError("Unable to initialize the database. Check the 'log.txt' file")
        else:
            log.debug("Database initialized correctly.")

    @classmethod
    def check_if_exists(cls, host: str, name: str):
        """
            A method for telling if such a product exists.
        :param host: the 'host' path.
        :param name: the product's name.
        :return: True if exists. False if it doesn't.
        """
        with DatabaseCursor(host) as cursor:
            log.debug("Checking if the product already exists or not.")
            cursor.execute("SELECT * FROM products WHERE name=?", (name.upper(), ))
            if cursor.fetchone():
                log.critical("The product already exists. You can't add more than one of each kind.")
                return True
            log.debug("The product doesn't exists.")
            return False

    def add_product(self, name: str, cost_price: float, sell_price: float, amount: int) -> bool:
        """
            Adds a new product to the inventory.
        :param name: product's name. It should be easy to remember
        :param cost_price: the price the vendor purchased it for.
        :param sell_price: the price the vendor want's to sell it for.
        :param amount: amount of this product in stock at the time of adding it to the list.
        :return: None
        """
        # Check if the product exists already and if the product doesn't exists, we start the adding process.
        if not Database.check_if_exists(self.host, name):
            try:
                log.debug("Adding the product")
                with DatabaseCursor(self.host) as cursor:
                    cursor.execute("INSERT INTO products VALUES(?, ?, ?, ?)", (name.upper(), cost_price, sell_price, amount))
            except Exception:
                log.critical("There was an error at adding the product.")
                raise UnableToAdd("We couldn't add the product.")
            else:
                log.debug(f"The product '{name.title()}' was added successfully.")
                return True
        else:
            log.error("Duplicated products are not permitted.")
            return False

    def update(self, name: str, cost_price: float, sell_price: float, in_stock: int) -> bool:
        """
            A method to update the features of a certain product.
        :param cost_price: The product's new cost.
        :param sell_price:  The product's new selling price.
        :param name: name of the product. The case doesn't matter, we convert it within the method.
        :param in_stock: the total number of objects encapsulated within this product's name.
        :return: True if it worked. False if it didn't.
        """
        if Database.check_if_exists(self.host, name):
            log.debug("Doing the updates one by one")
            try:
                # Updating the cost if needed
                if cost_price:
                    try:
                        log.debug(f"Updating '{name}' product's cost price.")
                        with DatabaseCursor(self.host) as cursor:
                            cursor.execute("UPDATE products SET cost_price=? WHERE name=?", (cost_price, name.upper()))
                    except OperationalError:
                        log.critical("Unable to update the 'cost_price' field. An OperationalError was raised by sqlite3.")
                        raise
                    else:
                        log.debug(f"'{name.upper()}' cost price updated successfully to $%.2f." % cost_price)

                # Updating the cost if needed
                if sell_price:
                    try:
                        log.debug(f"Updating '{name}' product's selling price.")
                        with DatabaseCursor(self.host) as cursor:
                            cursor.execute("UPDATE products SET sell_price=? WHERE name=?",
                                           (sell_price, name.upper()))
                    except OperationalError:
                        log.critical("Unable to update the 'sell_price' field. An OperationalError was raised by sqlite3.")
                        raise
                    else:
                        log.debug(f"'{name.upper()}' selling price updated successfully to $%.2f." % sell_price)

                # Updating 'in_stock'
                if in_stock:
                    try:
                        log.debug(f"Updating '{name}' in stock quantity.")
                        with DatabaseCursor(self.host) as cursor:
                            cursor.execute("UPDATE products SET in_stock=? WHERE name=?", (in_stock, name.upper()))
                    except OperationalError:
                        log.critical("Unable to update the 'in_stock' field. An OperationalError was raised by sqlite3.")
                        raise
                    else:
                        log.debug(f"'{name.upper()}' in stock quantity  updated successfully to {in_stock}.")
            except OperationalError:
                log.critical("Unable to update for some reason. An OperationalError was raised by sqlite3.")
            else:
                if cost_price or in_stock or sell_price:
                    log.debug("The updates were done successfully.")
                    return True
                else:
                    log.debug("The product wasn't updated, since it wasn't requested.")
                    return False
        else:
            log.error("The product wasn't found at all.")
            return False

    def remove_product(self, name: str) -> bool:
        """
            Deals with erasing a product given a name.
        :param name: The name of the product to erase.
        :return: True if it worked. False if it didn't.
        """
        if Database.check_if_exists(self.host, name.upper()):
            log.debug(f"'{name.upper()}' product found. Erasing it.")
            try:
                with DatabaseCursor(self.host) as cursor:
                    cursor.execute("DELETE FROM products WHERE name=?", (name.upper(), ))
            except OperationalError:
                log.critical("An OperationalError was raised by sqlite3.")
                return False
            else:
                log.debug(f"Product {name.upper()} removed successfully.")
                return True
        else:
            log.error("The product didn't exist at all.")
            return False

    # Here there are a few methods that will be useful for the front end.
    def get_products_names(self) -> List[str]:
        """
            Gets a list contaning the list of all product's names, ordered alphabetically.
        :return: List[str]
        """
        products_names = []
        log.debug("Getting the names for each product.")
        try:
            with DatabaseCursor(self.host) as cursor:
                cursor.execute("SELECT name FROM products ORDER BY name")
                result = cursor.fetchall()
                if result:
                    log.debug("There were results found. Loading them into the main list.")
                    for (name, ) in result:
                        products_names.append(name)
                    log.debug("List completed. Returning it.")
                    return products_names
                else:
                    log.error("There were no products at all.")
                    return []
        except OperationalError:
            log.critical("An OperationalError was raised by sqlite3.")

    def check_if_users(self):
        """
        Checks if the database holds records for users at all.
        :return: True if there are users. False if there aren't.
        """
        log.debug("Checking if there are users at all.")
        try:
            with DatabaseCursor(self.host) as cursor:
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
                if results:
                    log.debug("Apparently, there are users registered")
                    return True
                else:
                    log.error("There are no users in the database")
                    return False
        except OperationalError:
            log.critical("An OperationalError was raised by sqlite3.")

    def register_user(self, username: str, password: str):
        try:
            log.debug("Adding the new user.")
            with DatabaseCursor(self.host) as cursor:
                cursor.execute("INSERT INTO users VALUES(?, ?)", (username, password))
        except OperationalError:
            log.critical("An OperationalError was raised by sqlite3.")
        else:
            log.debug(f"The user '{username}' was added correctly")

    def check_login_info(self, username: str, password: str):
        try:
            log.debug("Checking if there's a username's match.")
            with DatabaseCursor(self.host) as cursor:
                cursor.execute("SELECT username FROM users WHERE username=?", (username,))
                results = cursor.fetchone()
                if results:
                    log.debug("There was a match for the username.")
                    cursor.execute("SELECT password FROM USERS where username=?", (username, ))
                    hashed_password = cursor.fetchone()[0]
                    if check_password_hash(hashed_password, password):
                        log.debug("The passwords match.")
                        return True
                    else:
                        log.error("There wasn't a match for the password.")
                        return False
                else:
                    log.error("There wasn't match for this username.")
        except OperationalError:
            log.critical("An OperationalError was raised by sqlite3.")