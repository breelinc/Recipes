from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
from flask_app.models.cooks_model import Cooks

#might need other imports like flash other classes and regex

db = 'recipes_and_cooks'

class Recipes:
    def __init__(self, data):
        self.recipe_id = data['recipe_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.cooked_date = data['cooked_date']
        self.thirty_minute = data['thirty_minute']
        self.cooks_cooks_id = data['cooks_cooks_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        #follow database table fields plus any other attribute you want to create
        

    @classmethod
    def get_recipes_data(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(db).query_db(query)
        recipes= []
        for data in results:
            recipes.append(cls(data))
        return recipes
    
    @classmethod
    def insert_recipes_data(cls,data):
        query = "INSERT INTO recipes (name,description,instructions,cooked_date,thirty_minute,cooks_cooks_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(cooked_date)s, %(thirty_minute)s, %(cooks_cooks_id)s);"
        result = connectToMySQL(db).query_db(query,data)
        return result
    
    @classmethod
    def get_recipe_id(cls, data):
        query = 'SELECT * FROM recipes JOIN cooks on recipes.cooks_cooks_id = cooks.cooks_id WHERE recipes.recipe_id = %(cooks_cooks_id)s;'
        results = connectToMySQL(db).query_db(query, data)
        print("results", results)
        cooks_dic = {
            "cooks_id" : results[0]["cooks_id"],
            "first_name" : results[0]["first_name"],
            "last_name" : results[0]["last_name"],
            "email" : results[0]["email"],
            "password" : results[0]["password"],
            "created_at" : results[0]["created_at"],
            "updated_at" : results[0]["updated_at"]
        }
        each_recipe = cls(results[0])
        each_recipe.creator = Cooks(cooks_dic)
        return each_recipe

    @classmethod
    def get_cook_by_email(cls,email):
        print("Email ---->", email)
        query = """SELECT * FROM cooks WHERE email = %(email)s;"""
        results =  connectToMySQL(db).query_db(query,email)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def get_all_recipes_by_cook(cls):
        query = """SELECT * FROM recipes LEFT JOIN cooks ON recipes.cooks_cooks_id = cooks.cooks_id;"""
        results = connectToMySQL(db).query_db(query)
        all_recipes_by_cook = []
        for row in results:
            one_recipe = cls(row)           #turning into class object
            #making Cooks dictionary
            one_recipe_cook_info = {
                'cooks_id' : row['cooks_id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['cooks.created_at'],
                'updated_at' : row['cooks.updated_at']
            }
            one_recipe.creator = Cooks(one_recipe_cook_info)
            all_recipes_by_cook.append(one_recipe)
        return all_recipes_by_cook

    
    @staticmethod
    def validate_recipe(recipe):
        valid = True
        if len(recipe["name"]) < 3:
            valid=False
            flash("Name must be at least 3 characters.")
        if len(recipe["description"]) < 3:
            valid=False
            flash("Description must be at least 3 characters.")
        if len(recipe["instructions"]) < 3:
            valid = False
            flash("Instructions must be at least 3 characters.")
        if recipe["cooked_date"] == "":
            valid = False
            flash("Date field must not be left blank.")
        if recipe["thirty_minute"] == "":
            valid = False
            flash("Must select an option for Under 30 minutes.")
        if valid:
            connectToMySQL(db).query_db("INSERT INTO cooks (name, description, instructions, cooked_date, thirty_minute, cooks_cooks_id) VALUES ( %(name)s, %(description)s, %(intructions)s, %(cooked_date)s, %(thirty_minute)s, %(cooks_cooks_id)s)", recipe)
                                        
    @classmethod
    def validate_update_recipe(cls,recipe):
        is_valid = True
        if len(recipe["name"]) < 3:
            flash("Name must be at least 3 characters.")
            is_valid=False
            print("name")
        if len(recipe["description"]) < 3:
            flash("Description must be at least 3 characters.")
            is_valid=False
            print("decription")
        if len(recipe["instructions"]) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
            print("instructions")
        if recipe["cooked_date"] == "":
            flash("Date field must not be left blank.")
            is_valid = False
            print("cooked_date")
        if recipe["thirty_minute"] == "":
            flash("Must select an option for Under 30 minutes.")
            is_valid = False
            print("thirty_minute")
        if is_valid:
            connectToMySQL(db).query_db("UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_date = %(cooked_date)s, thirty_minute = %(thirty_minute)s WHERE recipe_id = %(cooks_cooks_id)s", recipe)
        return is_valid
        
    @classmethod
    def delete_recipe(cls,data):
        query = "DELETE FROM recipes WHERE recipe_id = %(cooks_cooks_id)s;"
        result = connectToMySQL(db).query_db(query,data)
        return result