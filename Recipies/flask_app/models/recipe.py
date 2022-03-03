from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
from flask import flash

class Recipe():

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.date = data['date']
        self.description = data['description']
        self.instructions = data['instructions']
        self.sub30minutes = data['sub30minutes']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None


    @classmethod
    def create_recipe(cls, data):
        query = "INSERT INTO recipes (name, date, instructions, description, sub30minutes, user_id) VALUES (%(name)s, %(date)s, %(instructions)s, %(description)s, %(sub30minutes)s, %(user_id)s);"

        result = connectToMySQL('recipes_schema').query_db(query, data)

        return result

    @classmethod
    def get_all_recipes(cls):

        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"

        results = connectToMySQL('recipes_schema').query_db(query)

        recipes = []

        for item in results:
            new_recipe = Recipe(item)

            user_data = {
                'id': item['users.id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.created_at']
            }

            new_recipe.user = User(user_data)

            recipes.append(new_recipe)

        return recipes

    @classmethod
    def get_recipe_by_id(cls, data):

        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(id)s;"

        result = connectToMySQL('recipes_schema').query_db(query, data)

        recipe = Recipe(result[0])

        user_data = {
                'id': result[0]['users.id'],
                'first_name': result[0]['first_name'],
                'last_name': result[0]['last_name'],
                'email': result[0]['email'],
                'password': result[0]['password'],
                'created_at': result[0]['users.created_at'],
                'updated_at': result[0]['users.created_at']
            }

        recipe.user = User(user_data)

        return recipe

    @classmethod
    def update_recipe(cls, data):
        query = "UPDATE recipes SET name = %(recipe_name)s, date = %(recipe_date)s, description = %(recipe_description)s, instructions = %(recipe_instructions)s, sub30minutes = %(recipe_sub30minutes)s WHERE id = %(recipe_id)s"

        result = connectToMySQL('recipes_schema').query_db(query,data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        result = connectToMySQL('recipes_schema').query_db(query, data)


    @staticmethod
    def validate_recipe(data):
        is_valid = True

        if len(data['recipe_name']) < 3 or len(data['recipe_name']) > 100:
            is_valid = False
            flash("Recipe name should be atleast 3 characters long")

        if len(data['recipe_description']) < 3 or len(data['recipe_description']) > 500:
            is_valid = False
            flash("Recipe description should be atleast 3 characters long")

        if len(data['recipe_instructions']) < 3 or len(data['recipe_instructions']) > 500:
            is_valid = False
            flash("Recipe instructions should be at least 3 characters long")

        if data['recipe_date'] == '':
            is_valid = False
            flash("Recipe date must be filed")

        if "recipe_sub30minutes" not in data:
            is_valid = False
            flash("Does this take more tham 30 mintues to make?")

        return is_valid
