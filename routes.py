from app import app
from db import db
from flask import render_template, redirect, request
import functions, users

@app.route("/")
def index():
    all = functions.get_messages()
    return render_template("index.html", messages=all)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    username = request.form["username"]
    password = request.form["password"]
    if users.register(username, password):
        return redirect("/")
    return render_template("index.html", error="Rekisteröinti epäonnistui")

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    if users.login(username, password):
        return redirect("/")
    return render_template("/index.html", error="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/send", methods=["POST"])
def send():
    new = request.form["new_message"]
    if len(new) > 100:
        return render_template("/index.html", error="Viesti on liian pitkä")
    if functions.add_message(new):
        return redirect("/")
    return render_template("/index.html", error="Lähetys ei onnistunut")