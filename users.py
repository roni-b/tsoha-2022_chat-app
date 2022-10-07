import secrets
from db import db
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash

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
    try:
        del session["user_id"]
        del session["username"]
    except:
        return
    try:
        del session["receive"]
    except:
        pass

def get_users():
    sql = "SELECT username FROM users"
    result = db.session.execute(sql)
    return result.fetchall()

def check_user(username):
    sql = "SELECT username FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    print(user)
    if not user:
        return False
    return True

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def check_if_member(group_id):
    user = session["user_id"]
    sql = "SELECT * FROM groupMembers WHERE group_id=:group_id AND member_id=:user_id"
    result = db.session.execute(sql, {"group_id":group_id, "user_id":user})
    one_result = result.fetchone()
    if one_result == None:
        return False
    return True