import logging

from flask import Blueprint, render_template, redirect, url_for, session, flash, request
from blueprints.routes import inv_db

# Error handling
from utils.errors import NotAllowed, InvalidInput, ProductExists, NoProductsFound

products = Blueprint("products", __name__, static_folder="static", template_folder="template", url_prefix="/products")


# Create the logger
log = logging.getLogger("inventory_logger.products")


@products.route('/show_stock')
def show_stock():
    log.debug("Attempting to show stock. Checking if there's an active session.")
    try:
        if "user" in session:
            enumerated_products = inv_db.get_products_info()
            return render_template('show_stock.html', products=enumerated_products)
        else:
            raise NotAllowed("A session wasn't found.")
    except NotAllowed:
        log.error("Theres no session at the moment. This page can only be seen when there's an active session.")
        flash("Debe iniciar sesión para utilizar esa página.", 'error')
        return redirect(url_for('account.login'))


@products.route('/add_product', methods=['GET', 'POST'])
def add_product():
    log.debug("Attempting to show stock. Checking if there's an active session.")
    try:
        if request.method == 'GET':
            try:
                if "user" in session:
                    return render_template('add_product.html')
                else:
                    raise NotAllowed("A session wasn't found.")
            except NotAllowed:
                log.error("Attempted to load the 'add_product' page withouth a session.")
                flash("Debe iniciar sesión para utilizar esa página.", 'error')
                return redirect(url_for('account.login'))
        else:         
            try:
                log.debug("A post request was received. Checking if all inputs match.")
                product_name = request.form['product_name'].upper()
                cost_price = abs(float(request.form['cost_price']))
                sell_price = abs(float(request.form['sell_price']))
                in_stock = abs(int(request.form['in_stock']))
                log.debug("Adding the product to the database.")
                inv_db.add_product(product_name, cost_price, sell_price, in_stock)
            except ValueError:
                log.error("There was an error converting the inputs into they 'valid' type (float, int or str).")
                raise InvalidInput('At least one of the inputs submitted was invaild.')       
    except InvalidInput:
        log.error('One or more inputs are invalid.')
        flash('Una o más de las entradas fueron inválidas. Por favor, ingrese solo números para los precios y stock.\nUtilice el punto "." como separador decimal.','error')
        return redirect(url_for('products.add_product'))
    except ProductExists:
        log.critical("The product can't be added, since theres another with the same name.")
        flash("El nombre del producto coincide con otro ya almacenado. Los nombres deben ser únicos.", 'error')
        return redirect(url_for('products.add_product'))
    else:
        log.debug(f"The product'{product_name}' was added successfully")
        flash(f"'{product_name}' se agregó correctamente.", 'message')
        return redirect(url_for('products.add_product'))

@products.route('/remove_product', methods=['POST', 'GET'])
def remove_product():
    log.debug("Attempting to show stock. Checking if there's an active session.")
    try:
        if "user" in session:
            if request.method == "GET":
                products_names = inv_db.get_products_names()
                return render_template('remove_product.html', products_names=products_names)
            else:
                to_eliminate = request.form['product_name']
                log.debug(f"Received the order to eliminate '{to_eliminate}' from the database.")
                try:
                    inv_db.remove_product(to_eliminate)
                except NoProductsFound:
                    raise
                else:
                    log.debug(f"'{to_eliminate}' was erased successfully.")
                    flash(f"'{to_eliminate}' se eliminó correctamente de la base de datos.", 'message')
                    log.debug("Loading the products names once again.")
                    return render_template('remove_product.html', products_names=inv_db.get_products_names())
        else:
            raise NotAllowed("A session wasn't found.")
    except NotAllowed:
            log.error("Attempted to load the 'remove_products' page withouth a session.")
            flash("Debe iniciar sesión para utilizar esa página.", 'error')
            return redirect(url_for('account.login'))
    except NoProductsFound:
        log.error("There's no product with such name to delete.")
        flash("El nombre ingresado no coincide con el de ningún producto en la base de datos.", 'error')
        return redirect(url_for('products.show_stock'))
    
