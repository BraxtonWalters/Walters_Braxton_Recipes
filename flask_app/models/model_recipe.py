from flask_app import app, bcrypt, DATABASE, EMAIL_REGEX, NAME_REGEX, PASSWORD_REGEX
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import model_user
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.user_id = data["user_id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instruction = data["instruction"]
        self.under_30 = data["under_30"]
        self.date_made = data["date_made"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    # create
    @classmethod
    def create(cls, data):
        query = "INSERT INTO recipes (user_id, name, description, instruction, under_30, date_made) VALUES (%(user_id)s, %(name)s, %(description)s, %(instruction)s, %(under_30)s, %(date_made)s)"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # read
    #! This needs fixing we are returning a dictionary again. come on dum dum 
    @classmethod
    def get_all_recipes(cls):
        query = "SELECT * FROM recipes join users on users.id = recipes.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)


        all_recipes = []
        for user_dict in results:
            recipe_instance = cls(user_dict)
            user_data = {
                **user_dict,
                "id": user_dict["users.id"],
                "created_at": user_dict["users.created_at"],
                "updated_at": user_dict["users.updated_at"],
            }
            user_instance = model_user.User(user_data)
            recipe_instance.user = user_instance
            all_recipes.append(recipe_instance)
        return all_recipes

    
    # read
    @classmethod
    def get_by_id(cls, id):
        query = "SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, {"id": id})
        return results[0]
    
    # read
    @classmethod
    def get_one_recipe(cls, id):
        query = "SELECT * FROM recipes join users on users.id = recipes.user_id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, {"id": id})

        if not results:
            return []
        dict = results[0]
        recipe_instance = cls(dict)

        if dict["users.id"] != None:
            user_data = {
                "id": dict["users.id"],
                "created_at": dict["users.created_at"],
                "updated_at": dict["users.updated_at"],
                "first_name": dict["first_name"],
                "last_name": dict["last_name"],
                "email": dict["email"],
                "password": dict["password"]
            }
            user_instance = model_user.User(user_data)
            recipe_instance.user = user_instance
        return recipe_instance



        
    
    # update
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instruction = %(instruction)s, under_30 = %(under_30)s, date_made = %(date_made)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)
    
    # delete
    @classmethod
    def delete(cls, id):
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, {"id": id})
    
    # validate so crudv?
    @staticmethod
    def recipe_validator(data):
        is_valid = True

        if len(data["name"]) < 3:
            flash("Recipe name must be greater than 3 characters", "error_recipe_name")
            is_valid = False
        if len(data["description"]) < 3:
            flash("Recipe description must be greater than 3 characters", "error_recipe_description")
            is_valid = False
        if len(data["instruction"]) < 3:
            flash("Recipe instructions must be greater than 3 characters", "error_recipe_instruction")
            is_valid = False
        
        return is_valid