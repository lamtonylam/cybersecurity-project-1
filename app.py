from flask import Flask, request, render_template, redirect, url_for, session, flash
from flask import request
from logging.config import dictConfig

from db import Database
from modules.unsecure_passwords import check_if_password_is_unsecure

app = Flask(__name__)
app.secret_key = "your_secret_key_here"
db = Database()

from logging.config import dictConfig
from modules.logging_config import log_config

# A10:2017-Insufficient Logging & Monitoring
# to fix uncomment below
# dictConfig(log_config)


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # A2:2017-Broken Authentication
        # to fix uncomment below
        # if check_if_password_is_unsecure(password):
        #     flash(
        #         "Password is not safe, please choose another one that is not in the list of unsecure passwords."
        #     )
        #     return redirect(url_for("register"))

        if db.register_user(username, password):
            flash("Registration successful. Please log in.")
            # A10:2017-Insufficient Logging & Monitoring
            # to fix uncomment below
            # app.logger.warning(f"user {username} registered successfully")
            return redirect(url_for("login"))

        flash("Username already exists")
        # A10:2017-Insufficient Logging & Monitoring
        # to fix uncomment below
        # app.logger.warning(f"user {username} already exists")
        return redirect(url_for("register"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = db.authenticate_user(username, password)
        if user:
            session["user_id"] = user["id"]
            flash("Logged in successfully")
            # A10:2017-Insufficient Logging & Monitoring
            # to fix uncomment below
            # app.logger.warning(f"user {username} logged in successfully")
            return redirect(url_for("notes"))

        flash("Invalid username or password")
        # A10:2017-Insufficient Logging & Monitoring
        # to fix uncomment below
        # app.logger.error(f"Invalid username or password for user {username}")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("Logged out successfully")
    username = db.get_user_by_id(session["user_id"])["username"]
    # A10:2017-Insufficient Logging & Monitoring
    # to fix uncomment below
    # app.logger.warning(f"{username} logged out successfully")
    return redirect(url_for("login"))


@app.route("/notes", methods=["GET", "POST"])
def notes():
    if "user_id" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        content = request.form["content"]
        if db.add_note(session["user_id"], content):
            flash("Note added successfully")
            # A10:2017-Insufficient Logging & Monitoring
            # to fix uncomment below
            # app.logger.warning(f"Note added successfully")
        return redirect(url_for("notes"))

    user_notes = db.get_user_notes(session["user_id"])
    return render_template("notes.html", notes=user_notes)


@app.route("/admin", methods=["get"])
def admin():
    # A5:2017-Broken Access Control
    is_admin = request.args.get("is_admin")
    # to fix
    # uncomment this and comment above
    # is_admin = db.is_admin(session["user_id"]) if "user_id" in session else False

    ###
    ###

    # A10:2017-Insufficient Logging & Monitoring
    # to fix uncomment below
    # app.logger.warning(f"User {session['user_id']} is accessing admin page")

    return render_template("admin.html", is_admin=is_admin, notes=db.get_all_notes())


if __name__ == "__main__":
    app.run(debug=True)
