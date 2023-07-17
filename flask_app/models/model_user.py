from flask_app import app, bcrypt, DATABASE, EMAIL_REGEX, NAME_REGEX, PASSWORD_REGEX
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class User:
    def __init__(self, data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def create(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results
    
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT first_name, last_name, email FROM users WHERE id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query, data)
        return results[0]

    @staticmethod
    def validator_reg(data):
        is_valid = True
        
        if len(data["first_name"]) < 3:
            flash("Name must be longer than 2 characters", "error_users_first_name")
            is_valid = False
        if not NAME_REGEX.match(data["first_name"]):
            flash("Must contain only letters", "error_users_first_name")
            is_valid = False
        if len(data["last_name"]) < 3:
            flash("Name must be longer than 2 characters", "error_users_last_name")
            is_valid = False
        if not NAME_REGEX.match(data["last_name"]):
            flash("Must contain only letters", "error_users_last_name")
            is_valid = False

        if len(User.get_by_email(data)) >= 1:
            flash("Email already exists", "error_users_email")
            is_valid = False

        if not EMAIL_REGEX.match(data["email"]):
            flash("Email is not a valid email", "error_users_email")
            is_valid = False

        if not PASSWORD_REGEX.match(data["password"]):
            flash("Password must contain an uppercase and lower case letter, special character, and a number", "error_user_password")
            is_valid = False
        
        if data["password"] != data["confirm_password"]:
            flash("Passwords do not match dummy", "error2_user_password")
            is_valid = False

        if is_valid == True:
            flash("Great success", "success_user_reg")

        return is_valid
    
    @staticmethod
    def validator_login(data):
        is_valid = True
        if not User.get_by_email(data):
            flash("Email is not a registered email", "error_login_user_email")
            is_valid = False
        else:
            user_in_db = User.get_by_email(data)
            if not bcrypt.check_password_hash(user_in_db[0]["password"], data["password"]):
                flash("Wrong password bub", "error_password_user_password")
                is_valid = False

        return is_valid