import os
from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text


def login(name, password):
    sql = text("SELECT password, id, logs FROM users WHERE name = :name")
    result = db.session.execute(sql, {"name": name})
    user = result.fetchone()
    if not user:
        return False
    if not check_password_hash(user[0], password):
        return False
    session["user_id"] = user[1]
    session["user_name"] = name
    session["logs"] = user[2]
    session["csrf_token"] = os.urandom(16).hex()
    sql = text("SELECT logs FROM users WHERE name = :name")
    nrlogs = db.session.execute(sql, {"name": name}).fetchall()
    sql = text("UPDATE users SET logs = :logs WHERE name = :name")
    new_logs = str(int(int(nrlogs[0][0]) + 1))
    db.session.execute(sql, {"logs": new_logs, "name": name})
    db.session.commit()
    return True

def logout():
    del session["user_id"]
    del session["user_name"]
    del session["logs"]

def register(name, password, logs):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (name, password, logs) VALUES (:name, :password, :logs)")
        db.session.execute(sql, {"name": name, "password": hash_value, "logs": logs})
        db.session.commit()
    except:
        return False
    return login(name, password)

def user_id():
    return session.get("user_id", 0)

def require_role(role):
    if role > session.get("logs", 0):
        abort(403)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)