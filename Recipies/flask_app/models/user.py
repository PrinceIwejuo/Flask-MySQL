from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re

class User():

    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def create_new_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"

        result =connectToMySQL("recipes_schema").query_db(query, data)

        return result

    @classmethod
    def get_user_by_email(cls, data):

        query = "SELECT * FROM users WHERE email = %(email)s"

        results = connectToMySQL("recipes_schema").query_db(query, data)

        if len(results) == 0:
            return False
        
        else:
            return User(results[0])

        return results 

    @staticmethod
    def validate_new_user(data):
        is_valid = True

        email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

        if User.get_user_by_email(data):
            is_valid = False 
            flash("Email should be unique")

        if len(data['first_name']) < 3 or len(data['first_name']) > 45:
            is_valid = False
            flash("First name should be 3 to 45 characters long")

        if len(data['last_name']) < 3 or len(data['last_name']) > 45:
            is_valid = False
            flash("Last name should be 3 to 45 characters long")

        if not email_regex.match(data['email']):
            is_valid = False
            flash("Email adress is not formatted correctly.")
        
        if len(data['password']) < 8:
            is_valid = False
            flash("Passwrod should be atleast eight characters long")
        
        if not data['password'] == data['confirm_password']: 
            is_valid = False
            flash("Password and confirm password does not match")
        
        return is_valid

