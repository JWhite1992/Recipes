from flask_app import app
from flask_app.controllers.controllers_cooks import Cook
from flask_app.controllers.controllers_recipes import Recipe

if __name__ == "__main__":
    app.run(debug=True)
