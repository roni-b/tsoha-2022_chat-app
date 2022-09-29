from app import app
from db import db
from flask import render_template, redirect, request
import functions, users

@app.route("/")
def index():
    all_messages = functions.get_messages()
    all_users = users.get_users()
    all_groups = functions.get_groups()
    return render_template("index.html", messages=all_messages, users=all_users,
    groups=all_groups)

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) or len(password) < 3:
            render_template("index.html", error="Tunnus tai salasana liian lyhyt")
        if users.register(username, password):
            return redirect("/")
        return render_template("index.html", error="Rekisteröinti epäonnistui")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
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
