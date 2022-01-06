from recipe_app import DB
from recipe_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.under_30_minutes = data['under_30_minutes']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.chef_id = data['chef_id']
        self.recipe = None

    # add recipe static:-----------

    @staticmethod
    def validate_recipe(data):
        is_Valid = True
        if len(data['name']) < 3:
            flash("Name must be at least 3 characters.", 'name')
            is_Valid = False
        # if len(data['under_30_minutes']) < 1:
        #     flash("Is this a quick meal?", 'under_30_minutes')
            is_Valid = False
        if len(data['description']) < 6:
            flash("Please tell us more about this recipe.", 'description')
            is_Valid = False
        if len(data['instructions']) < 6:
            flash("Please tell us what's in this recipe.", 'instructions')
            is_Valid = False
        if len(data['date_made']) < 6:
            flash("When did you make this?", 'date_made')
            is_Valid = False

        return is_Valid


# create recipe-------------------------

    @classmethod
    def add_recipe(cls, data):
        query = "INSERT INTO recipe ( name, under_30_minutes, description, instructions, date_made, chef_id) VALUES (%(name)s, %(under_30_minutes)s, %(description)s, %(instructions)s, %(date_made)s, %(chef_id)s);"
        new_recipe_id = connectToMySQL(DB).query_db(query, data)
        return new_recipe_id

# show one recipe-----------------------

    @classmethod
    def show_one_recipe(cls, data):
        query = "SELECT * FROM recipe WHERE id = %(id)s;"
        results = connectToMySQL(DB).query_db(query, data)
        return cls(results[0])

# get all recipes-------------------------
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipe;"
        return connectToMySQL(DB).query_db(query)

# Delete----------------------------
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipe WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)

# Update----------------------------

    @classmethod
    def update(cls, data):
        query = "UPDATE recipe SET name=%(name)s, under_30_minutes=%(under_30_minutes)s, description=%(description)s, instructions=%(instructions)s, date_made = NOW() WHERE id = %(id)s;"
        return connectToMySQL(DB).query_db(query, data)
