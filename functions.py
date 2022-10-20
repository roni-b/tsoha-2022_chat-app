from db import db
import routes
from flask import session, request
import users
from datetime import datetime, timedelta

def get_messages():
    try:
        sql = ("SELECT M.id, M.content, M.sent_at, U.username FROM messages AS M, users AS U, groupMembers AS G WHERE G.group_id=:groups_id AND G.member_id=:user_id AND M.user_id=U.id AND M.groups_id=:groups_id ORDER BY M.id")
        result = db.session.execute(sql, {"groups_id":session["receive"], "user_id":session["user_id"]})
        return result.fetchall()
    except:
        sql = ("SELECT M.id, M.content, M.sent_at, U.username FROM messages AS M, users AS U, groupMembers AS G WHERE G.member_id=:user_id AND M.user_id=U.id ORDER BY M.id")
        result = db.session.execute(sql, {"user_id":session["user_id"]})
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

def add_message_for_all(new):
    dif = timedelta(hours=3)
    now = datetime.now()
    time = now + dif
    sql = "INSERT INTO publicMessages (content, sent_at) VALUES (:content, :sent_at)"
    db.session.execute(sql, {"content": new, "sent_at": time})
    db.session.commit()

def get_public_messages():
    sql = "SELECT * FROM publicMessages"
    result = db.session.execute(sql)
    return result.fetchall()

def delete_message(id):
    sql = ("DELETE FROM messages WHERE id=:id")
    db.session.execute(sql, {"id": id})
    db.session.commit()

def edit_message(id, new):
    sql = "UPDATE messages SET content=:new WHERE id=:id"
    db.session.execute(sql, {"new": new, "id": id})
    db.session.commit()

def exit_group():
    group_id = session["receive"]
    user_id = session["user_id"]
    sql = ("DELETE FROM groupMembers WHERE member_id=:member_id AND group_id=:group_id")
    db.session.execute(sql, {"group_id":group_id, "member_id":user_id})
    db.session.commit()
    update_group_name()
    del session["receive"]

def update_group_name():
    group_id = session["receive"]
    username = session["username"]
    sql = ("SELECT name FROM groups WHERE id=:group_id")
    result = db.session.execute(sql, {"group_id": group_id})
    old = result.fetchone()
    str_old = str(old)
    new = str_old.replace(username, "")
    strip_new = str(new).strip(",('')'")
    sql = ("UPDATE groups SET name=:new WHERE id=:group_id")
    db.session.execute(sql, {"new":strip_new, "group_id": group_id})
    db.session.commit()

def search(query):
    sql = ("SELECT M.content, M.sent_at, U.username FROM users AS U, messages AS M, groupMembers AS G, groups AS R WHERE G.member_id=:user_id AND R.id=G.group_id AND M.groups_id=G.group_id AND U.id=M.user_id ORDER BY M.id;")
    result = db.session.execute(sql, {"query":"%"+query+"%", "user_id": session["user_id"]})
    sql_results = result.fetchall()
    proper_results = []
    for result in sql_results:
        if query.lower() in result[0].lower():
            proper_results.append(result)
    return proper_results

def vote(rate, id):
    sql = "SELECT message_id FROM messageRatings WHERE message_id=:message_id"
    result = db.session.execute(sql, {"message_id": id})
    if result.fetchone() == None:
        sql = "INSERT INTO messageRatings (message_id) VALUES (:message_id)"
        db.session.execute(sql, {"message_id": id})
        db.session.commit()
    if rate:
        sql = "UPDATE messageRatings SET likes=likes+1 WHERE message_id=:message_id"
        db.session.execute(sql, {"message_id": id})
        db.session.commit()
    if not rate:
        sql = "UPDATE messageRatings SET dislikes=dislikes+1 WHERE message_id=:message_id"
        db.session.execute(sql, {"message_id": id})
        db.session.commit()

def get_votes(id):
    sql = "SELECT likes, dislikes FROM messageRatings WHERE message_id=:id"
    result = db.session.execute(sql, {"id": id})
    results = result.fetchall()
    return results

def report(id):
    sql = "SELECT message_id FROM reports WHERE message_id=:message_id"
    result = db.session.execute(sql, {"message_id": id})
    if result.fetchone() == None:
        sql = "INSERT INTO reports (message_id) VALUES (:message_id)"
        db.session.execute(sql, {"message_id": id})
        db.session.commit()
    sql = "UPDATE reports SET report_count=report_count+1 WHERE message_id=:message_id"
    db.session.execute(sql, {"message_id": id})
    db.session.commit()