from db import db
import routes
from flask import session, request
import users
from datetime import datetime, timedelta

def get_messages():
    try:
        sql = ("SELECT content, sent_at, user_id FROM messages WHERE groups_id=:groups_id;")
        result = db.session.execute(sql, {"groups_id":session["receive"]})
        return result.fetchall()
    except:
        sql = ("SELECT content, sent_at FROM messages;")
        result = db.session.execute(sql)
        return result.fetchall()
        
def get_messages2(user, group):
    #sql = ("SELECT content, sent_at, user_id FROM messages WHERE groups_id=:groups_id")
    pass

def get_groups():
    sql = ("SELECT name FROM groups;")
    result = db.session.execute(sql)
    return result.fetchall()

def get_group_id(members):
    sql = ("SELECT id FROM groups WHERE name=:name;")
    result = db.session.execute(sql, {"name":members})
    return result.fetchone()

def add_group(members):
    try:
        sql = ("INSERT INTO groups (name) VALUES (:name)")
        db.session.execute(sql, {"name":members})
        db.session.commit()
        sql = ("SELECT id FROM groups WHERE name=:name")
        result = db.session.execute(sql, {"name":members})
        group_id = result.fetchone()
        listMembers = members.split(",")
        for member in listMembers:
            user_id = users.get_user_id(member)
            if not add_member(group_id, user_id):
                return False
        return True
    except:
        #print("addgroup errorr") 
        return False

def add_member(group_id, user_id):
    try:
        group_id_s = str(group_id).strip(",()")
        user_id_s = str(user_id).strip(",()")
        sql = ("INSERT INTO groupMembers (group_id, member_id) VALUES (:group_id, :member_id)")
        db.session.execute(sql, {"group_id":group_id_s, "member_id":user_id_s})
        db.session.commit()
        return True
    except:
        #print("addmembererror")
        return False

def add_message(new):
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            return False
        user_id = users.user_id()
        if len(new) > 0:
            dif = timedelta(hours=3)
            now = datetime.now()
            time = now + dif
            try:
                group_id = session["receive"]
                sql = "INSERT INTO messages (content, sent_at, user_id, groups_id) VALUES (:new_message, :sent_at, :user_id, :groups_id)"
                db.session.execute(sql, {"new_message":new, "sent_at":time, "user_id":user_id, "groups_id":group_id})
                db.session.commit()
                return True
            except:
                pass
            return True
        return False
    except: 
        return False



