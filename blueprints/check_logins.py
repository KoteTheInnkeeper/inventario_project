import logging

from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash
from blueprints.routes import db
# Setting the blueprint.
check_logins = Blueprint("check_logins", __name__, static_folder="static", template_folder="template", url_prefix="/login")

log = logging.getLogger('inventory_project.check_logins')


# Define routes
@check_logins.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if db.check_login_info(username, password):
            session['user'] = username
            log.debug(f"There was a match. The user '{username}' was successfully logged in.")
        else:
            log.error("There wasn't a full match on the username and password provided.")
        return redirect(url_for('routes.home'))
    else:
        return "<h1>Tasintentando loguear y estás en login.html EN GET </h1>"


@check_logins.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if not "user" in session:
            new_username = request.form['username']
            hashed_password = generate_password_hash(request.form['password'], method="sha256")
            try:
                db.register_user(new_username, hashed_password)
            except Exception:
                log.critical("An exception happened.")
            else:
                log.debug("User successfully registered. Redirecting to the homepage.")
                return redirect(url_for('routes.home'))
    else:
        return "<h1>Tasintentando crear y estás en login.html EN GET </h1>"


@check_logins.route('/signout')
def signout():
    log.debug("Trying to logout")
    if "user" in session:
        session.pop('user', None)
        log.debug("Successfully logged out. Returning to home")
    else:
        log.error("There was no user to logout.")
    return redirect(url_for('routes.home'))



