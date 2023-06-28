from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.models_cook import Cook
from flask_app.models.models_recipe import Recipe

@app.route('/dashboard')
def dashboard():
    if 'cook_id' not in session:
        return redirect('/')
    cook = Cook.get_one({'id': session['cook_id']})  # Retrieve the cook from the database based on the cook_id stored in the session
    recipes = Recipe.get_all_with_cooks() # Retrieve all recipes with their associated cooks from the database
    return render_template('dashboard.html', cook=cook, recipes=recipes)

@app.route('/new/recipe')
def new_recipe():
    cooks = Cook.get_all() # Retrieve all cooks from the database
    meals = Recipe.get_all_with_cooks() # Retrieve all recipes with their associated cooks from the database
    return render_template('create_recipes.html', cooks=cooks, meals=meals)

@app.route('/recipes/view/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'cook_id' in session:
        recipe = Recipe.get_one_recipe_with_cook({"id": recipe_id})  # Retrieve a specific recipe with its associated cook from the database based on the recipe_id
        if recipe:
            return render_template('recipes.html', recipe=recipe, cook=recipe.cook)
        else:
            flash("Recipe not found.")
    else:
        flash("You must be logged in to view a recipe.")
    return redirect('/dashboard')

@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'cook_id' in session:
        data = {
            'name': request.form['name'],
            'description': request.form['description'],
            'instructions': request.form['instructions'],
            'date': request.form['date'],
            'under30': 1 if 'under30' in request.form else 0,
            'cook_id': session['cook_id']
        }
        recipe_id = Recipe.save(data)  # Save the new recipe to the database and retrieve the generated recipe ID
        flash("Recipe created successfully.", "success")
        return redirect('/dashboard')
    else:
        flash("You must be logged in to create a recipe.", "error")
        return redirect('/')

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    edit_recipe_id = {
        'id': recipe_id
    }
    recipe = Recipe.get_one_recipe_with_cook(edit_recipe_id) # Retrieve a specific recipe with its associated cook from the database based on the recipe_id
    if recipe:
            return render_template('edit_recipes.html', meal=recipe)    
    else:
        flash("Recipe not found.")
        return redirect('/dashboard')

@app.route('/recipes/update/<int:recipe_id>', methods=['POST'])
def edited_recipe(recipe_id):
    if 'cook_id' in session:
        recipe = Recipe.get_one_recipe_with_cook({"id": recipe_id}) # Retrieve a specific recipe with its associated cook from the database based on the recipe_id
        if recipe and recipe.cook_id == session['cook_id']:
            data = {
                'id': recipe_id,
                'name': request.form['name'],
                'description': request.form['description'],
                'instructions': request.form['instructions'],
                'date': request.form['date'],
                'under30': 1 if 'under30' in request.form else 0,
            }
            Recipe.update(data) # Update the recipe in the database with the new data
            flash("Recipe updated successfully.", "success")
            return redirect('/dashboard')
        else:
            flash("Recipe not found or you don't have permission to update it.")
            return redirect('/dashboard')
    else:
        flash("You must be logged in to update a recipe.")
        return redirect('/')

@app.route('/recipes/<int:recipe_id>', methods=['GET'])
def one_recipe(recipe_id):
    recipe = Recipe.get_one(recipe_id)  # Retrieve a specific recipe with its associated cook from the database based on the recipe_id
    if recipe:
        return render_template('recipes.html', recipe=recipe)
    else:
        flash("Recipe not found.", "error")
        return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>/delete', methods=['POST'])
def delete_recipe(recipe_id):
    data = {"id": recipe_id}
    Recipe.delete(data) # Delete the recipe from the database based on the recipe_id
    return redirect('/dashboard')
