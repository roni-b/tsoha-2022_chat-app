from db import db
import routes
from flask import session, request
import users
from datetime import datetime, timezone, timedelta

def get_messages():
    sql = ("SELECT content, sent_at FROM messages;")
    result = db.session.execute(sql)
    return result.fetchall()

def add_message(new):
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            return False
        user_id = users.user_id()
        if len(new) > 0:
            utc3 = timedelta(hours=3)
            time = datetime.now(timezone(utc3))
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
