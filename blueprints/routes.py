import logging

from flask import Blueprint, render_template, redirect, url_for, session
from databases.database_management import Database


routes = Blueprint("routes", __name__, static_folder="static", template_folder="template", url_prefix="")
# Create the logger
log = logging.getLogger("inventory_logger.routes")

# Create the Database object
INVENTORY_DATABASE = './databases/database.db'
db = Database(INVENTORY_DATABASE)


@routes.route('/home')
@routes.route('/')
def home():
    log.debug("Telling apart if there are users registered at all")
    users_exist = db.check_if_users()
    return render_template("home.html", session=session, users_exist=users_exist)




@routes.route('/epicum')
def test():
    return "<h1>EPICARDOOOO</h1>"
