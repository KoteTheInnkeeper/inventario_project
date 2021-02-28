from flask import Blueprint, render_template, redirect, url_for

routes = Blueprint("routes", __name__, static_folder="static", template_folder="template", url_prefix="")


@routes.route('/home', methods=['POST', 'GET'])
@routes.route('/')
def home():
    return render_template("home.html")


@routes.route('/login', methods=['GET', 'POST'])
def login():
    return "<h1>Tasintentando loguear y estás en login.html </h1>"

@routes.route('/epicum')
def test():
    return "<h1>EPICARDOOOO</h1>"
