import logging

from flask import Blueprint, render_template, redirect, url_for, session, flash
from blueprints.routes import inv_db

# Error handling
from utils.errors import NotAllowed

products = Blueprint("products", __name__, static_folder="static", template_folder="template", url_prefix="/products")


# Create the logger
log = logging.getLogger("inventory_logger.products")


@products.route('/show_stock')
def show_stock():
    log.debug("Attempting to show stock. Checking if there's an active session.")
    try:
        if "user" in session:
            products = inv_db.get_products_info
            return render_template('show_stock.html', products=products)
        else:
            raise NotAllowed("A session wasn't found.")
    except NotAllowed:
        log.error("Theres no session at the moment. This page can only be seen when there's an active session.")
        return redirect(url_for('account.login'))


@products.route('/add_product')
def add_product():
    log.debug("Attempting to show stock. Checking if there's an active session.")
    try:
        if "user" in session:
            return render_template('add_product.html')
        else:
            raise NotAllowed("A session wasn't found.")
    except NotAllowed:
        log.error("Attempted to load the 'add_product' page withouth a session.")
        return redirect(url_for('account.login'))


@products.route('/remove_product')
def remove_product():
    log.debug("Attempting to show stock. Checking if there's an active session.")
    try:
        if "user" in session:
            return render_template('add_product.html')
        else:
            raise NotAllowed("A session wasn't found.")
    except NotAllowed:
        log.error("Attempted to load the 'remove_products' page withouth a session.")
        return redirect(url_for('account.login'))
