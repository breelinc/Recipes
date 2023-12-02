from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.cooks_model import Cooks
from flask_app.models.recipes_model import Recipes


@app.route('/add_recipe') #Get request for 127.0.0.1:5000
def add_recipe():
    return render_template('new_recipes.html', cooks = Cooks.get_cook_data())

@app.route('/added_recipe', methods=['POST']) #Post request route
def added_recipe():
    data = { "name": request.form['name'],
            "description": request.form['description'],
            "instructions": request.form['instructions'],
            "cooked_date": request.form['cooked_date'],
            "thirty_minute": request.form['thirty_minute'],
            "cooks_cooks_id": session['cooks_id']
            }
    Recipes.insert_recipes_data(data)
    return redirect('/recipes')

@app.route('/recipes')
def show_recipes():
    return render_template('recipes.html', all_recipes = Recipes.get_all_recipes_by_cook())

# @app.route('/cook/<int:cooks_id>')
# def cook_profile(cooks_id):
#     profile_cooks_id = {'cooks_id': cooks_id}
#     return render_template('recipes.html', cook = Cooks.get_cooks_with_recipes_by_cooks_id(profile_cooks_id))

@app.route('/view_recipe') #Get request for 127.0.0.1:5000
def view_recipe():
    return render_template('recipe_post.html', cook = Cooks.get_cook_data())

@app.route('/recipes/<int:recipe_id>')
def display_recipe(recipe_id):
    ids = {
        "cooks_cooks_id": recipe_id
    }
    return render_template('view_recipes.html', recipe = Recipes.get_recipe_id(ids))

@app.route('/recipes/edit/<int:recipe_id>')
def edit_recipe(recipe_id):
    data = {
        'cooks_cooks_id' : recipe_id
    }
    session['recipe_id'] = recipe_id
    return render_template('edit_recipe.html', recipe = Recipes.get_recipe_id(data))

@app.route('/update_recipe', methods =['POST'])
def update_recipe():
    data = { "name": request.form['name'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "cooked_date": request.form['cooked_date'],
        "thirty_minute": request.form['thirty_minute'],
        "cooks_cooks_id": session['recipe_id']
        }
    print("HELLLOOOO")
    is_valid = Recipes.validate_update_recipe(data)
    if is_valid:
        return redirect('/recipes')
    return redirect('/recipes/edit/'+ str(session['recipe_id'])) 

@app.route('/delete_recipe/<int:recipe_id>') #Post request route
def delete_recipe(recipe_id):
    data = {
            "cooks_cooks_id": recipe_id
            }
    Recipes.delete_recipe(data)
    return redirect('/recipes')