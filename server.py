from flask_app import app
#! import controllers OMG PLEASE IMPORT THE CONTROLLERSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
from flask_app.controllers import controller_route, controller_recipe, controller_user


if __name__ == "__main__":
    app.run(debug=True)