
from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User
from flask_app.models.recipe import Recipe

@app.route('/recipes')
def recipes():
    recipes = Recipe.get_all_recipes()
    print(recipes)
    return render_template('recipes.html', recipes = recipes)

@app.route('/recipes/new')
def new_recipe():
    
    return render_template('new_recipe.html')

@app.route('/recipe/create', methods =['POST'])
def create_recipe():

    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    data = {
        'name': request.form['recipe_name'],
        'date': request.form['recipe_date'],
        'description': request.form['recipe_description'],
        'instructions': request.form['recipe_instructions'],
        'sub30minutes': request.form['recipe_sub30minutes'],
        'user_id': session['user_id'],
    }
    
    Recipe.create_recipe(data)
    return redirect('/recipes')

@app.route('/recipes/<int:recipe_id>')
def single_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('single_recipe.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/edit')
def edit_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    recipe = Recipe.get_recipe_by_id(data)
    return render_template('recipe_edit.html', recipe = recipe)

@app.route('/recipes/<int:recipe_id>/update', methods= ['POST'])
def update_recipe(recipe_id):
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/{recipe_id}/edit')

    else:
        data ={
            'recipe_id': recipe_id,
            'recipe_name': request.form['recipe_name'],
            'recipe_date': request.form['recipe_date'],
            'recipe_description': request.form['recipe_description'],
            'recipe_instructions': request.form['recipe_instructions'],
            'recipe_sub30minutes': request.form['recipe_sub30minutes']
        }
        Recipe.update_recipe(data)
        print("validation for edit works great")
        return redirect(f'/recipes/{recipe_id}')

@app.route('/recipes/<int:recipe_id>/delete')
def delete_recipe(recipe_id):
    data = {
        'id': recipe_id
    }
    Recipe.delete_recipe(data)
    return redirect('/recipes')