from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import musicians
from flask import flash
import re
# from flask_bcrypt import Bcrypt        
# bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
LETTER_REGEX = re.compile(r'^[a-zA-Z]+$')

DATABASE = "favorite_musicians"

class User:
    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#this saves and inserts each new user created in the registration form
    @classmethod
    def save(cls,data):
        query= "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s, NOW(), NOW());"
        return connectToMySQL(DATABASE).query_db(query,data)

# I want this to select the logged in user and display their first name in the h1 tag of dashboard, but this currently does not work.
    @classmethod
    def get_one_user(cls,data):
        query = "SELECT * FROM users WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

#this method is selecting the user by its id so that I am able to display all the user's favorite artist on one page
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users LEFT JOIN musicians ON users.id = musicians.user_id WHERE users.id = %(id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        user = User(results[0])
        list_of_musicians = []
        for row in results:
            musician_data = {
                **row,
                'id': row['musicians.id'],
                'first_name': row['musicians.first_name'],
                'last_name': row['musicians.last_name'],
                'created_at': row['musicians.created_at'],
                'updated_at': row['musicians.updated_at']
            }
            this_musician = musicians.Musician(musician_data)
            list_of_musicians.append(this_musician)
        user.musicians_posted = list_of_musicians
        return user

#checks if email already exists in the database
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

#validates and seperates each error message by category
    @staticmethod
    def validate(data_data):
        is_valid = True
        if len(data_data['first_name']) < 2:
            is_valid = False
            flash("First name must be at least 2 characters long", "err_first_name")
        elif not LETTER_REGEX.match(data_data['first_name']):
            flash("First name must only be letters", "err_first_name")
            is_valid = False 
        if len(data_data['last_name']) < 2:
            is_valid = False
            flash("Last name must be at least 2 characters long", "err_last_name")
        elif not LETTER_REGEX.match(data_data['last_name']):
            flash("Last name must only be letters", "err_last_name")
            is_valid = False 
        if not EMAIL_REGEX.match(data_data['email']): 
            flash("Invalid email address!", "err_email")
            is_valid = False
        else:
            data ={
                'email': data_data['email']
            }
            potential_user = User.get_by_email(data)
            if potential_user:
                is_valid = False
                flash("This email is already taken", "err_email")
        if len(data_data['password']) < 8:
            is_valid = False
            flash("Password must be at least 8 characters long", "err_password")
        elif not data_data['password'] == data_data['confirm_password']:
            is_valid = False
            flash("Passwords don't match", "err_password")
        return is_valid

