from flask_app import app
from flask import render_template, redirect, request, session

# landing
@app.route("/")
def landing():
    return render_template("index.html")