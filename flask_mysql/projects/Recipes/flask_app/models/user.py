from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import recipe
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# model the class after the user table from our database
class User:
    db = "recipes_schema"
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(User.db).query_db( query, data)

    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(User.db).query_db(query, user)
        print(user)
        if len(user['first_name']) < 2:
            flash("First name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash("Last name must be at least 2 characters.", "register")
            is_valid = False
        if len(results) >= 1:
            flash("Email already in use.","register")
            is_valid=False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Password must be at least 8 characters.", "register")
            is_valid = False
        if user['password'] != user['cpassword']:
            flash("Passwords don't match.","register")
            is_valid = False
        return is_valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query,data)
        print(query)
        print (results)
        # Didn't find a matching user
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return cls(result[0])

    # @classmethod
    # def get_user_with_recipes( cls , data ):
    #     query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
    #     results = connectToMySQL(User.db).query_db( query , data )
    #     user = cls( results[0] )
    #     for column in results:
    #         sighting_data = {
    #             "id" : column["recipes.id"],
    #             "location" : column["location"],
    #             "comment" : column["comment"],
    #             "date_of_sighting" : column["date_of_sighting"],
    #             "num_sasquatches" : column["num_sasquatches"],
    #             "first_name" : column["first_name"],
    #             "last_name" : column["last_name"]
    #         }
    #         user.sightings.append(sighting_data)
    #     print(user.sightings)
    #     return user.sightings[0]

    @classmethod
    def get_users_with_recipes(cls):
        query = "SELECT * FROM users LEFT JOIN recipes ON recipes.user_id = users.id;"
        results = connectToMySQL(User.db).query_db( query )
        users_recipes = []
        for row_from_db in results:
            data = {
                "first_name" : row_from_db['first_name'],
                "last_name" : row_from_db['last_name'],
                "recipe_id" : row_from_db["recipes.id"],
                "name" : row_from_db["name"],
                "under" : row_from_db["under"],
                "user_id" : row_from_db["id"]
            }
            users_recipes.append(data)
        return users_recipes