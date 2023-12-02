from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
#might need other imports like flash other classes and regex

db = 'recipes_and_cooks'

class Cooks:
    def __init__(self, data):
        self.cooks_id = data['cooks_id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        #follow database table fields plus any other attribute you want to create
        


    @staticmethod
    def validate_cook(cook):
        is_valid = True
        # test whether a field matches the pattern
        if len(cook['first_name']) < 2:
            flash("Name must be at least 2 characters.","first_name")
            is_valid = False
        if len(cook['last_name']) < 2:
            flash("Name must be at least 2 characters.","last_name")
            is_valid = False
        if not EMAIL_REGEX.match(cook['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(cook['password']) < 8:
            flash("Name must be at least 8 characters.","password")
            is_valid = False
        if len(cook['confirm_password']) < 3:
            flash("Name must be at least 3 characters.","ConfirmPassword")
            is_valid = False
            print('_____________________')
        return is_valid
    
    @classmethod
    def insert_cook_data(cls,data):
        print("data", data)
        query = """INSERT INTO cooks (first_name, last_name, email, password) 
                VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s );"""
        results = connectToMySQL(db).query_db(query,data)
        #Nice little head start
        #Rest of code here
        print(results)
        return results
    
    @classmethod
    def get_cooks_id(cls, data):
        query = 'SELECT * FROM cooks WHERE cooks_id = %(cooks_id)s;'
        results = connectToMySQL(db).query_db(query, data)
        print("results", results)
        return cls(results[0])
    
    @classmethod
    def get_email(cls, data):
        query = 'SELECT * FROM cooks WHERE email = %(email)s;'
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        print('____________________________')
        return cls(results[0])
    
    @classmethod
    def get_cook_data(cls):
        query = "SELECT * FROM cooks;"
        results = connectToMySQL(db).query_db(query)
        cook = []
        for cooks in results:
            cook.append(cls(cooks))
        return cook
    
    @classmethod
    def cook_profile(cls,id):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(db).query_db(query)
        recipes = []
        for data in results:
            recipes.append(cls(data))
    
    @classmethod
    def get_cooks_with_recipes_by_cooks_id(cls,data):
        query = """SELECT * FROM cooks left JOIN recipes on cooks.cooks_id = recipes.cooks_cooks_id WHERE cooks_id = %(cooks_id)s;"""
        results =  connectToMySQL(db).query_db(query,data)
        cook = cls(results[0])
        for recipe in results:
            new_recipe = recipe(recipe)
            cook.recipes.append(new_recipe)
        print(results)
        return cook