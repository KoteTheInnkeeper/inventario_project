import logging

from flask import Blueprint, render_template, redirect, url_for, request, session
from werkzeug.security import generate_password_hash
from blueprints.routes import inv_db, user_db
from login_info.login_management import UserDatabase
# Setting the blueprint.
account = Blueprint("account", __name__, static_folder="static", template_folder="template", url_prefix="/user")

log = logging.getLogger('inventory_project.check_logins')


# Define routes
@account.route('/', methods=['GET', 'POST'])
@account.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        usermatch, passmatch = user_db.check_login(username, password)
        if usermatch and passmatch:
            session['user'] = username.lower()
            log.debug(f"There was a match. The user '{username}' was successfully logged in.")
            return f"<h1>Bienvenido, {session['user']}</h1>"
        elif usermatch:
            log.error("The username was correct, but the password wasn't.")
            return "<h1>Contraseña incorrecta</h1>"
        return "<h1>No hay una cuenta registrada con ese usuario.</h1>"
    else:
        return "<h1>Tasintentando loguear y estás en login.html EN GET </h1>"


@account.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        if not "user" in session:
            new_username = request.form['username']
            hashed_password = generate_password_hash(request.form['password'], method="sha256")
            try:
                user_db.new_user(new_username, hashed_password)
            except Exception:
                log.critical("An exception happened.")
                raise
            else:
                log.debug("User successfully registered. Redirecting to the homepage.")
                return redirect(url_for('routes.home'))
    else:
        return "<h1>Tasintentando crear y estás en login.html EN GET </h1>"


@account.route('/signout')
def signout():
    log.debug("Trying to logout")
    if "user" in session:
        session.pop('user', None)
        log.debug("Successfully logged out. Returning to home")
    else:
        log.error("There was no user to logout.")
    return redirect(url_for('routes.home'))



