from flask import render_template, request, redirect, session
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models import user

@app.route("/recipes")
def home():
    if 'user_id' not in session:
        return redirect('/logout')
    users_recipes = user.User.get_users_with_recipes()
    id = session['user_id']
    return render_template("dashboard.html", users_recipes=users_recipes, id=id)

@app.route('/recipes/new')
def new_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('add.html',  user = user.User.get_by_id(data))

@app.route('/add_recipe', methods=["POST"])
def add_recipe():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "date_created" : request.form["date_created"],
        "under": request.form["under"],
        "user_id": session["user_id"]
    }
    Recipe.save(data)
    return redirect('/recipes')

@app.route('/destroy/<int:id>')
def destroy(id):
    data = {
        "id":id
    }
    Recipe.destroy(data)
    return redirect('/recipes')

@app.route("/recipes/edit/<int:id>")
def edit(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": id
    }
    print("hi", data)
    recipe = Recipe.get_one_recipe(data)
    print("testinggg",recipe.id)
    return render_template("edit.html", recipe=recipe)

@app.route('/edit_recipe', methods=['POST'])
def update():
    print("helooooo", request.form)
    id = request.form['id']
    if not Recipe.validate_recipe(request.form):
        return redirect(f'/recipes/edit/{id}')
    Recipe.update(request.form)
    return redirect('/recipes')

@app.route('/show/<int:id>')
def show(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={ 
        "id":id
    }
    recipe=Recipe.get_recipe_with_user(data)
    print(recipe)
    return render_template("show.html", recipe=recipe)

# @app.route('/show/None')
# def create_new_from_none():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     return redirect('/new/tree')

# @app.route('/destroy/None')
# def create_new_from_none_2():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     return redirect('/new/tree')

# @app.route('/edit/None')
# def create_new_from_none_3():
#     if 'user_id' not in session:
#         return redirect('/logout')
#     return redirect('/new/tree')

if __name__ == "__main__":
    app.run(debug=True)