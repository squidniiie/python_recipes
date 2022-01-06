from recipe_app import DB, bcrypt
import re
from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class Chef:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

# register---------------

    @staticmethod
    def validate_user(data):
        is_Valid = True
        if len(data['first_name']) < 2:
            flash("First name must be at least 2 characters.", 'first_name')
            is_Valid = False
        if len(data['last_name']) < 2:
            flash("Last name must be at least 2 characters.", 'last_name')
            is_Valid = False
        if len(data['email']) < 6:
            flash("Email must be at least 2 characters.", 'email')
            is_Valid = False
        if len(data['password']) < 6:
            flash("Password must be at least 2 characters.", 'password')
            is_Valid = False
        return is_Valid

    # login static:-----------

    @staticmethod
    def validate_login(data):
        is_Valid = True
        if len(data['email']) < 6:
            flash("Email must be at least 2 characters.", 'email')
            is_Valid = False
        if len(data['password']) < 6:
            flash("Password must be at least 2 characters.", 'password')
            is_Valid = False
        return is_Valid

    # login action-----------

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM chef WHERE "
        wheres = []
        for key in data:
            wheres.append(f"{key}=%({key})s")
        where_str = ' AND '.join(wheres)
        query += where_str + ';'
        results = connectToMySQL(DB).query_db(query, data)
        print(results)
        if results:
            return cls(results[0])

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM chef WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return cls(results[0])

    # register:---------------

    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO chef (first_name, last_name, email, password) VALUES (%(first_name)s,%(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(DB).query_db(query, data)
