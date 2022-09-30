from db import db
import routes
from flask import session, request
import users
from datetime import datetime, timedelta

def get_messages():
    sql = ("SELECT content, sent_at FROM messages;")
    result = db.session.execute(sql)
    return result.fetchall()

def get_messages2():
    #return messages
    pass

def get_groups():
    sql = ("SELECT name FROM groups;")
    result = db.session.execute(sql)
    return result.fetchall()

def add_group(new):
    user_id = users.user_id()
    sql = ("INSERT INTO groups (name) VALUES (:name)")
    db.session.execute(sql, {"name":new})

def add_member(group_id, member_id):
    sql = ("INSERT INTO groupMembers (group_id, member_id) VALUES (:group_id, :member_id)")
    db.session.execute(sql, {"group_id":group_id, "member_id":member_id})

def add_message(new):
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            return False
        user_id = users.user_id()
        if len(new) > 0:
            dif = timedelta(hours=3)
            now = datetime.now()
            time = now + dif
            sql = "INSERT INTO messages (content, sent_at, user_id) VALUES (:new_message, :sent_at, :user_id)"
            db.session.execute(sql, {"new_message":new, "sent_at":time, "user_id":user_id})
            db.session.commit()
            return True
        return False
    except: 
        #if len(new) > 0:
            #sql = "INSERT INTO messages (content, sent_at) VALUES (:new_message, NOW())"
            #db.session.execute(sql, {"new_message":new})
            #db.session.commit()
            #return True
        return False

