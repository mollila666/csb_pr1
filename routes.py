from app import app
from flask import render_template, request, redirect, abort
import threads
import users
from flask import session


@app.route("/")
def index():
    return render_template("index.html", messages=threads.get_all_messages(), users=threads.get_users())

@app.route("/send_message_to_user", methods=["post"])
def send_message_to_users():
#    if session["csrf_token"] != request.form["csrf_token"]:
#        abort(403)
    if session["user_name"]:
        message = request.form["new_message"]
        threads.send_message_to_user(message)
        return redirect("/")

@app.route("/login", methods=["get", "post"])
def login():
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if not users.login(username, password):
            return render_template("error.html", message="Incorrect username or password")
#        if threads.get_nrlogs(username) == 1:
#            users.logout()
#            return render_template("changepass.html", username=username, reason='First time log in')        
#        if len(password) < 8:
#            users.logout()
#            return render_template("changepass.html", username=username, reason='Password not ok')
        return redirect("/")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/changep", methods=["get", "post"])
def changep():
    if request.method == "GET":
        return render_template("changepass.html")

    if request.method == "POST":
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        username = request.form["username"]
        if len(password1) < 0:
            return redirect("/")
#        elif len(password1) < 8:
#            return redirect("/")
        else:
            threads.modify_passw(username,password1)
            return redirect("/")

@app.route("/register", methods=["get", "post"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 1 or len(username) > 20:
            return render_template("error.html", message="The username must contain 1-20 characters.")

        password1 = request.form["password1"]
        password2 = request.form["password2"]
        if password1 != password2:
            return render_template("error.html", message="Passwords differ")
        if password1 == "":
            return render_template("error.html", message="The password is empty")

        if threads.check_users(username) > 0:
            return render_template("error.html", message="The username is already in use, please choose another username.")

        if not users.register(username, password1,logs=0):
            return render_template("error.html", message="Username registration failed")
        return redirect("/logout")


