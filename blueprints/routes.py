import logging

from flask import Blueprint, render_template, redirect, url_for, session
from databases.inventory_management import Database
from login_info.login_management import UserDatabase

routes = Blueprint("routes", __name__, static_folder="static", template_folder="template", url_prefix="")
# Create the logger
log = logging.getLogger("inventory_logger.routes")

# Create the Database object for inventory
INVENTORY_DATABASE = './databases/database.db'
inv_db = Database(INVENTORY_DATABASE)

# Create the Database object for the users
USERS_DATABASE = './login_info/users.db'
user_db = UserDatabase(USERS_DATABASE)

@routes.route('/home')
@routes.route('/')
def home():
    log.debug("Telling apart if there are users registered at all")
    users_exist = user_db.check_if_users()
    return render_template("home.html", session=session, users_exist=users_exist)

@routes.route('/epicum')
def test():
    return "<h1>EPICARDOOOO</h1>"
