from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Cook:
    db='cook_book'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @classmethod
    def save(cls, data):  # Save the cook data to the database and retrieve the generated cook ID
        query = """
        INSERT INTO cooks (first_name, last_name, email, password)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);
        """
        cook_id = connectToMySQL(cls.db).query_db(query, data)
        return cook_id

    @classmethod
    def get_by_email(cls, email):  # Retrieve the cook from the database based on the email
        query = "SELECT * FROM cooks WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, {'email': email})
        if results:
            return cls(results[0])
        return None

    @classmethod
    def get_one(cls, data): # Retrieve a single cook from the database based on the ID
        query = "SELECT * FROM cooks WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if results:
            return cls(results[0])

    @classmethod
    def get_all(cls): # Retrieve all cooks from the database
        query = "SELECT * FROM cooks;"
        results = connectToMySQL(cls.db).query_db(query)
        cooks = []
        for row in results:
            cooks.append(cls(row))
        return cooks
    
    @staticmethod
    def validate_registration(data): #Validate registration
        is_valid = True 
        if len(data['first_name']) < 1:
            flash("First name must be at least 1 character.")
            is_valid = False
        if len(data['last_name']) < 1:
            flash("Last name must be at least 1 character.")
            is_valid = False
        if not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(data['password']) < 8:
            flash("Password must be at least 8 characters.")
            is_valid = False
        if not data['password'] != data['confirm_password']:
            flash("Passwords do not match")
            is_valid = False
        return is_valid

    
    @staticmethod
    def validate_login(data): #Validate user when logging in
        is_valid = True
        if len(data['email']) < 1:
            flash("Email field must not be empty.")
            is_valid = False
        if len(data['password']) < 1:
            flash("Password field must not be empty.")
            is_valid = False
        return is_valid
