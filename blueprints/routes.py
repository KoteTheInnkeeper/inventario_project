import logging

from flask import Blueprint, render_template, redirect, url_for, session, flash
from databases.inventory_management import Database
from login_info.login_management import UserDatabase
from utils.errors import NotAllowed

# Error handling
from utils.errors import NotAllowed

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
    try:
        log.debug("Accessing the home page. Checking if there's a session currently.")
        if not ("user" in session):
            raise NotAllowed('No active session found')
        else:
            return render_template('home.html')
    except NotAllowed:
        log.error("An active session wasn't found. Redirecting to the 'login' page.")
        if user_db.check_if_users():
            flash("Debe iniciar sesión para utilizar la página.", 'error')
        else:
            flash("Debe registrar un usuario. La página no puede utilizarse si no se inicia sesión.", 'error')
        return redirect(url_for('account.login'))


@routes.route('/epicum')
def test():
    return "<h1>EPICARDOOOO</h1>"
