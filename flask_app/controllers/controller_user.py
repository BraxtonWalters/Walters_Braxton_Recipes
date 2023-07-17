from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
from flask_app.models.model_user import User
from flask_app.models.model_recipe import Recipe


# user account registration 
@app.route("/user/create", methods=["POST"])
def user_reg():
    if not User.validator_reg(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {**request.form}
    data["password"] = pw_hash
    user_id = User.create(data)
    session["user_id"] = user_id
    return redirect("/recipes")


# recipes render route 
@app.route("/recipes")
def user_display():
    user = User.get_user_by_id({"id": session["user_id"]})
    session["user"] = user
    recipes = Recipe.get_all_recipes()
    return render_template("recipe_wall.html", user=user, recipes=recipes)


# user login
@app.route("/user/login", methods=["POST"])
def user_login():
    if not User.validator_login(request.form):
        return redirect("/")
    
    user_id = User.get_by_email(request.form)
    session["user_id"] = user_id[0]["id"]
    return redirect('/recipes')


# user logout
@app.route("/user/logout")
def logout():
    session.clear()
    return redirect("/")