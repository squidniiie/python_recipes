from recipe_app import app
from flask import render_template, redirect, request, session, flash, url_for
from recipe_app.models.recipe import Recipe
from recipe_app.models.chef import Chef

# display:-----------------------------


@app.route('/dashboard')
def recipes_index():
    all_recipes = Recipe.get_all()
    data = {
        'id': session['id']
    }
    one_chef = Chef.get_one(data)
    return render_template("dashboard.html", all_recipes=all_recipes, one_chef=one_chef)


@app.route('/recipe/<int:id>')
def show_one_recipe(id):
    data = {"id": id
            }
    one_recipe = Recipe.show_one_recipe(data)
    chef_data = {
        "id": session['id']
    }
    return render_template("recipe_show.html", one_recipe=one_recipe, chef=Chef.get_by_id(chef_data))


@app.route('/new_recipe')
def new_recipe():
    data = {
        'id': session['id']
    }
    one_chef = Chef.get_one(data)
    return render_template("create_recipe.html", one_chef=one_chef)

# show individual recipe:


@app.route('/edit_recipe/<int:id>')
def editrecipe(id):
    data = {
        **request.form,
        "id": id
    }
    chef_data = {
        "id": session['id']
    }
    return render_template("/edit_recipe.html", edit_recipe=Recipe.show_one_recipe(data), chef=Chef.get_by_id(chef_data))


# action:--------------------------------


@app.route('/add_recipe', methods=['POST'])
def add_recipe():
    data = {
        **request.form,
        'chef_id': session['id']
    }
    if not Recipe.validate_recipe(data):
        return redirect(url_for('new_recipe'))
    Recipe.add_recipe(data)
    return redirect('/dashboard')

# delete:--------------------------------


@app.route('/delete/recipe/<int:id>')
def delete(id):
    data = {'id': id
            }
    Recipe.delete(data)
    return redirect('/dashboard')

#  update:-----------------------------------


@app.route('/update_recipe', methods=['POST'])
def update():
    id = request.form['id']
    data = {
        "id": id,
        "name": request.form['name'],
        "under_30_minutes": request.form['under_30_minutes'],
        "description": request.form['description'],
        "instructions": request.form['instructions'],
        "date_made": request.form['date_made'],
    }
    if not Recipe.validate_recipe(data):
        return redirect(f"/edit_recipe/{id}")
    # url_for('editrecipe')

    Recipe.update(data)
    return redirect('/dashboard')
