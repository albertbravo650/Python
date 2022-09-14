from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash

class Recipe:
    db = "recipes_schema"
    def __init__(self , db_data ):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.instructions = db_data['instructions']
        self.date_created = db_data['date_created']
        self.under = db_data['under']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.recipes = []

    @classmethod
    def save( cls , data ):
        query = "INSERT INTO recipes (name, description, instructions, date_created, under, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_created)s, %(under)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(Recipe.db).query_db( query, data)

    # @classmethod
    # def get_all(cls):
    #     query = "SELECT * FROM recipes;"
    #     results = connectToMySQL(Recipe.db).query_db(query)
    #     recipes = []
    #     for recipe in results:
    #         recipes.append(cls(recipe))
    #     return recipes

    @classmethod
    def get_one_recipe(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        print(data)
        result = connectToMySQL(Recipe.db).query_db(query, data)
        print(result)
        return cls(result[0])

    # @classmethod
    # def get_date(cls, data):
    #     query = "SELECT DATE_FORMAT(date_planted, '%M %e, %Y') FROM trees WHERE id = %(id)s;"
    #     result = connectToMySQL(Tree.db).query_db(query, data)
    #     print(result)
    #     return cls(result[0])

    @staticmethod
    def validate_recipe(recipe):
        print(recipe)
        is_valid = True # we assume this is true
        if len(recipe['name']) < 3:
            flash("Enter name of recipe, atleast 3 characters", "add_recipe")
            is_valid = False
        if len(recipe['description']) < 3:
            flash("Enter a description, atleast 3 characters", "add_recipe")
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash("Enter instructions, atleast 3 characters", "add_recipe")
            is_valid = False
        if (recipe['under']) == '':
            flash("Check under 30 min y/n", "add_recipe")
            is_valid = False
        if (recipe['date_created']) == '':
            flash("Enter date cooked/made", "add_recipe")
            is_valid = False
        return is_valid

    @classmethod
    def destroy(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(Recipe.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s, date_created=%(date_created)s, under=%(under)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(Recipe.db).query_db(query, data)

    @classmethod
    def get_recipe_with_user( cls , data ):
        query = "SELECT * FROM recipes LEFT JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"
        results = connectToMySQL(Recipe.db).query_db( query , data )
        # user = cls( results[0] )
        recipe_user = []
        print("bleh", results)
        for column in results:
            recipe_data = {
                "id" : column["id"],
                "name" : column["name"],
                "description" : column["description"],
                "instructions" : column["instructions"],
                "date_created" : column["date_created"],
                "under" : column["under"],
                "first_name" : column["first_name"],
                "last_name" : column["last_name"]
            }
            recipe_user.append(recipe_data)
            print("newtesting",recipe_user)
        return recipe_user[0]