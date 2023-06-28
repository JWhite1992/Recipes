from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.models_cook import Cook
from flask_app.models.models_recipe import Recipe
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])  # Encrypt password
    confirm_pw_hash = bcrypt.generate_password_hash(request.form['confirm_password'])  # Encrypt confirm_password
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash,
        'confirm_password': confirm_pw_hash  # Store hashed confirm_password
    }
    if Cook.validate_registration(data): # Validate the registration data
        cook_id = Cook.save(data)  # Save the cook data to the database and retrieve the generated cook ID
        session['cook_id'] = cook_id # Store the cook ID in the session
        flash("Registration successful. Please log in.", "success")
        return redirect('/dashboard')
    else:
        return redirect('/')



@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
    data = {
        'email': email,
        'password': password
    }
    if Cook.validate_login(data): #Validate login
        cook = Cook.get_by_email(email) # Retrieve the cook from the database based on the email
        if cook is None or not bcrypt.check_password_hash(cook.password, password): # Check if the cook or password is invalid
            flash("Invalid email or password. Please try again.", "error")
            return redirect('/')
        session['cook_id'] = cook.id # Store the cook ID in the session
        return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/logout')
def logout():
    session.clear()  # Clear the session data
    flash('Logged out successfully!', 'success')
    return redirect('/')


