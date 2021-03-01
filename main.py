import logging

# The database we use for the inventory_class.
from databases.inventory_management import Database
# Flask app things.
from flask import Flask, redirect, render_template, url_for, session
from blueprints.routes import routes
from blueprints.account import account
from datetime import timedelta

# Setting the log file.
log = logging.getLogger('inventory_logger.main_app')


# Flask
log.debug("Initializing the Flask app.")
app = Flask(__name__)
app.register_blueprint(routes)
app.register_blueprint(account)
app.secret_key = "J@tAYGpzdCRL6C2jKBuW&8"
app.permanent_session_lifetime = timedelta(hours=8)
log.debug('Permanent session lifetime set')


# Running the app
if __name__ == '__main__':
    app.run(debug=True)


