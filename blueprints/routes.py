from flask import Blueprint, render_template, redirect, url_for

routes = Blueprint("routes", __name__, static_folder="static", template_folder="template", url_prefix="")


@routes.route('/home')
@routes.route('/')
def home():
    return render_template("home.html")


@routes.route('/test')
def test2():
    return "<h1>test</h1>"

@routes.route('/epicum')
def test():
    return "<h1>EPICARDOOOO</h1>"
