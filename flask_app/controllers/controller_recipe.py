from flask_app import app, bcrypt
from flask import render_template, redirect, request, session
#! import the model!!!! 
#! Is this going to cause a circular import issue??? 
#! Happens only in a model file
from flask_app.models.model_recipe import Recipe
from flask_app.models.model_user import User


# create recipe render
#! swap create and new
@app.route("/recipe/create")
def create_recipe():
    if "user_id" not in session:
        return redirect("/")
    return render_template("create_recipe.html")

# create recipe route
@app.route("/recipe/new", methods=["POST"])
def new_recipe():
    data = {**request.form}
    if not Recipe.recipe_validator(data):
        return redirect("/recipe/create")
    Recipe.create(data)
    return redirect("/")

# edit recipe render
@app.route("/recipe/edit/<int:id>")
def edit_recipe(id):
    if "user_id" not in session:
        return redirect("/")
    recipe = Recipe.get_by_id(id)
    return render_template("edit_recipe.html", recipe=recipe)

# update recipe route
@app.route("/recipe/updated/<int:id>", methods=["POST"])
def recipe_updated(id):
    data = {**request.form}
    data["id"] = id
    if not Recipe.recipe_validator(data):
        return redirect(f"/recipe/edit/{id}")
    Recipe.update(data)
    return redirect("/recipes")

# delete recipe route 
#! any recipe could be deleted
@app.route("/recipe/delete/<int:id>")
def recipe_delete(id):
    Recipe.delete(id)
    return redirect("/recipes")

# view recipe render
@app.route("/recipe/view/<int:id>")
def recipe_view(id):
    recipe = Recipe.get_one_recipe(id)
    user = User.get_user_by_id({"id": session["user_id"]})
    return render_template("view_recipe.html", recipe=recipe, user=user)