from flask_app import app
from flask import render_template, redirect, session

# landing
@app.route("/")
def landing():
    if "user_id" not in session:
        return render_template("index.html")
    return redirect('/recipes')
        