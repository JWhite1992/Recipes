from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.models_cook import Cook

class Recipe:
    db='cook_book'
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under30 = data['under30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.cook_id = data['cook_id'] 
        self.cook= None # Initializing the 'cook' attribute as None

    @classmethod
    def save(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under30, cook_id) " \
                "VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under30)s, %(cook_id)s);"
        recipe_id = connectToMySQL(cls.db).query_db(query, data)
        return recipe_id

    @classmethod
    def update(cls, data):
        query = f"UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, " \
                "date = %(date)s, under30 = %(under30)s, updated_at = NOW() WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def get_one_recipe_with_cook(cls, data):
        query ="""
        SELECT * FROM recipes JOIN cooks ON recipes.cook_id = cooks.id
        WHERE recipes.id = %(id)s;
        """  
        results =connectToMySQL(cls.db).query_db(query, data) #any get query and all query is going to become a list 
        print("recipes_get_one_cook_with_recipe", results)
        one_recipe_class = cls(results[0]) #making a class out of the first item in the result list starting at index 0
        print("onerecipe models recipes", one_recipe_class)
        one_cook_info ={
            'id': results[0]['id'],
            'first_name' : results[0]['first_name'],
            'last_name' : results[0]['last_name'],
            'email' : results[0]['email'],
            'password' : results[0]['password'],
            'created_at' : results[0]['created_at'],
            'updated_at' : results[0]['updated_at']
        }
        one_cook_class = Cook(one_cook_info) # Creating an instance of the Cook class using the retrieved cook information
        print("one cook class models recipes",one_cook_class)
        one_recipe_class.cook = one_cook_class # Assigning the Cook object to the cook attribute of the Recipe object
        print("one_recipe_class.cook in models recipe", one_recipe_class.cook)
        return one_recipe_class

    @classmethod
    def get_all_with_cooks(cls):
        query = """
        SELECT * FROM recipes JOIN cooks ON recipes.cook_id = cooks.id;
        """
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        if results:
            for row in results:
                recipe = cls(row)
                cook_info = {
                    'id': row['cooks.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'password': row['password'],
                    'created_at': row['cooks.created_at'],
                    'updated_at': row['cooks.updated_at']
                }
                cook = Cook(cook_info) # Creating an instance of the Cook class using the retrieved cook information
                recipe.cook = cook # Assigning the Cook object to the cook attribute of the Recipe object
                recipes.append(recipe)
        return recipes

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for row in results:
            recipes.append(cls(row))# Executing an SQL SELECT query to retrieve all recipes
        return recipes
    

