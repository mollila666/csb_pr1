from sqlalchemy.sql import text
from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash

def modify_passw(username,password):
    hash_value = generate_password_hash(password)
    sql = text("UPDATE users SET password = :password WHERE name = :username")
    db.session.execute(sql, {"password": hash_value, "username": username})
    db.session.commit()
    sql = text("UPDATE users SET logs = :logs WHERE name = :username")
    db.session.execute(sql, {"logs": 2, "username": username})
    db.session.commit()
    return ' '

def get_all_messages():
    if "user_name" in session.keys():
        sql = text("SELECT message FROM messages WHERE name = :username")
        messages = db.session.execute(sql, {"username": session["user_name"]}).fetchall()
        return messages

def send_message_to_user(message):
    sql = "SELECT name FROM users"
    users=db.session.execute(text(sql)).fetchall()
    for user in users:
        sql = "INSERT INTO messages (name,message) VALUES ('%s','%s');" %(user[0],message)
        db.session.execute(text(sql))
#        Hello Sir'); DROP TABLE messages;--
#        sql = text("INSERT INTO messages (name, message) VALUES (:name, :message)")
#        db.session.execute(sql, {"name": user[0], "message": message})
        db.session.commit()
    return ' '

def get_nrlogs(user):
    sql = text("SELECT logs FROM users WHERE name = :username")
    nr_of_logs = db.session.execute(sql, {"username": user}).fetchall()
    return nr_of_logs[0][0]

def get_users():
    sql = "SELECT name, id FROM users ORDER BY name"
    users=db.session.execute(text(sql)).fetchall()
    return users

def check_users(username):
    sql = text("SELECT name FROM users WHERE name = :username")
    temp = db.session.execute(sql, {"username": username}).fetchall()
    return len(temp)

