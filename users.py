import secrets
from db import db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from secrets import token_hex

def register(username, password):
    hash_value = generate_password_hash(password)
    sql = "INSERT INTO users (password, username) VALUES (:password, :username)"
    db.session.execute(sql, {"password":hash_value, "username":username})
    db.session.commit()
    return login(username, password) 

def login(username, password):
    sql = "SELECT id, password, admin FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["csrf_token"] = secrets.token_hex(16)
            session["user_id"] = user[0]
            session["username"] = username
            return True
        return False

def logout():
    del session["user_id"]
    del session["username"]

def user_id():
    try:
        return session["user_id"]
    except:
        return False

def username():
    try:
        return session["username"]
    except:
        return False

def admin():
    try:
        return session["admin"]
    except:
        return False
       
def get_users():
    sql = "SELECT username FROM users"
    result = db.session.execute(sql)
    return result.fetchall()

