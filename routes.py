from app import app
from db import db
from flask import render_template, redirect, request, session
import functions, users

@app.route("/")
def index():
    try:
        all_users = users.get_users()
        all_groups = functions.get_groups()
        return render_template("index.html", users=all_users, groups=all_groups)
    except: 
        return render_template("index.html")

@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.check_user(username):
            return render_template("error.html", error="Tunnus on jo olemassa")
        if len(username) < 3 or len(password) < 3:
            return render_template("error.html", error="Tunnus tai salasana liian lyhyt")
        if users.register(username, password):
            return redirect("/")
        return render_template("error.html", error="Rekisteröinti epäonnistui")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if len(username) == 0 or len(password) == 0:
            return render_template("error.html", error="Tunnus tai salasana ei voi olla tyhjä")
        if users.login(username, password):
            return redirect("/")
        return render_template("error.html", error="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/send", methods=["POST"])
def send():
    new = request.form["new_message"]
    if len(new) > 100:
        return render_template("error.html", error="Viesti on liian pitkä")
    if len(new) == 0:
        return render_template("error.html", error="Viesti ei voi olla tyhjä")
    if functions.add_message(new):
        return redirect("/")
    return render_template("error.html", error="Lähetys ei onnistunut, todennäköisesti et ole ryhmän jäsen tai et ole valinnut ryhmää")

@app.route("/new_conversation", methods=["POST"])
def newConversation():
    choises = request.form.getlist("choices")
    if len(choises) == 0:
        return redirect("/")
    usernames = ",".join(choises) 
    if functions.add_group(usernames):
        return redirect("/")
    return render_template("error.html", error="Ryhmän luonti ei onnistunut, samanlainen ryhmä voi olla jo olemassa")

@app.route("/conversation", methods=["POST", "GET"])
def conversation():
    if request.method == "GET":
        print(request.form["delete_group"])
    members = request.form["group"]
    who_receive = functions.get_group_id(members)
    who_receive_s = str(who_receive).strip(",()")
    session["receive"] = who_receive_s
    return redirect("/")

@app.route("/messages")
def messages():
    try:
        query = request.args["edit"]
        id = request.args["id"]
        username = request.args["username"]
        if username != session["username"]:
            return redirect("/")
        if query[0] == "P":
            functions.delete_message(id)
        functions.edit_message(id)
    except: 
        pass
    all_messages = functions.get_messages()
    return render_template("messages.html", allMessages=all_messages)

@app.route("/exit_group")
def exit_group():
    functions.exit_group()
    return redirect("/")

@app.route("/search")
def search():
    query = request.args["query"]
    results = functions.search(query)
    if len(results) > 0:
        return render_template("results.html", results=results)
    return render_template("error.html", error="Ei tuloksia hakusanalla")
