from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.cooks_model import Cooks
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app) #importing the class here
#There will be other imports need depending what you're trying to use in this file
#You will also need a bycrypt import (we will introduce this week 5)


@app.route('/') #Get request for 127.0.0.1:5000
def home():
    return render_template('index.html')

@app.route('/register_cook', methods=['POST']) #Post request route
def registered_cook():
    if not Cooks.validate_cook(request.form):
        flash('This needs to be corrected.', 'register_cook')
        return redirect('/')
    data = {"first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": bcrypt.generate_password_hash(request.form['password'])
            }
    cooks_id = Cooks.insert_cook_data(data)
    session['cooks_id'] = cooks_id
    return redirect('/recipes')

@app.route('/login', methods=['POST']) #Post request route
def logged_in_cook():
    each_cook = Cooks.get_email(request.form)
    if not each_cook:
        flash('Invalid Email', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(each_cook.password, request.form['password']):
        flash('Invalid Password', 'login')
        return redirect('/')
    session['cooks_id'] = each_cook.cooks_id
    return redirect('/recipes')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')