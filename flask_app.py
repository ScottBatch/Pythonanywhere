from flask import Flask, redirect, render_template, session, request
from os import urandom

app = Flask(__name__)



app.secret_key = urandom(16)


@app.route("/")
def index():
    if not session.get("user_id"):
        return redirect("/login")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["user_id"] = request.form.get("username")
        return redirect("/")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session["user_id"] = None
    return redirect("/")