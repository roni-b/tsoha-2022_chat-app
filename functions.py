from db import db
import routes
from flask import session, request
import users
from datetime import datetime, timedelta

def get_messages():
    try:
        sql = ("SELECT M.content, M.sent_at, U.username FROM messages AS M, users AS U, groupMembers AS G WHERE G.group_id=:groups_id AND G.member_id=:user_id AND M.user_id=U.id AND M.groups_id=:groups_id ORDER BY M.id")
        result = db.session.execute(sql, {"groups_id":session["receive"], "user_id":session["user_id"]})
        return result.fetchall()
    except:
        sql = ("SELECT content, sent_at FROM messages WHERE groups_id=NULL;")
        result = db.session.execute(sql)
        return result.fetchall()

def get_groups():
    sql = ("SELECT N.name FROM groups AS N, groupMembers AS G WHERE G.member_id=:user_id AND N.id=G.group_id;")
    result = db.session.execute(sql, {"user_id":session["user_id"]})
    return result.fetchall()

def get_group_id(members):
    sql = ("SELECT id FROM groups WHERE name=:name;")
    result = db.session.execute(sql, {"name":members})
    return result.fetchone()

def get_group_name():
    sql = ("SELECT name FROM groups WHERE id=:id")
    result = db.session.execute(sql, {"id":session["receive"]})
    return result.fetchone()

def add_group(new_members):
    try:
        members = session["username"]+","+new_members
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
        print("addgroup error") 
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
        print("addmember error")
        return False

def add_message(new):
    try:
        if session["csrf_token"] != request.form["csrf_token"]:
            return False
        group_id = session["receive"]
        user_id = session["user_id"]
        if not users.check_if_member(group_id):
            return False
        dif = timedelta(hours=3)
        now = datetime.now()
        time = now + dif
        sql = "INSERT INTO messages (content, sent_at, user_id, groups_id) VALUES (:new_message, :sent_at, :user_id, :groups_id)"
        db.session.execute(sql, {"new_message":new, "sent_at":time, "user_id":user_id, "groups_id":group_id})
        db.session.commit()
        return True
    except: 
        return False