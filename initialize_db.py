from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
#app.secret_key = ''

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
#app.config["SQLALCHEMY_DATABASE_URI"] = ''
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

def add_user(username):
    password = username
    hash_value = generate_password_hash(password)
    name = username
    role = 0
    sql = text("INSERT INTO users (name, password, logs) VALUES (:name, :password, :role)")
    with app.app_context():
        db.session.execute(sql, {'name': name, 'password': hash_value, 'role': role})
        db.session.commit()

add_user('admin')
add_user('user1')
add_user('user2')