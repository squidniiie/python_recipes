from recipe_app import app, DB, bcrypt
from flask import render_template, redirect, request, session, flash
from recipe_app.models.chef import Chef

# display ----------------------------------


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/dashboard')
def dashboard():
    if 'id' not in session:
        return redirect('/')
    one_chef = Chef.get_by_id({'id': session['id']})
    return render_template("dashboard.html", one_chef=one_chef)
# action------------------------------------


@app.route('/register', methods=['POST'])
def add_user():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': request.form['password'],
    }
    if not Chef.validate_user(data):
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data['password'] = pw_hash
    new_chef_id = Chef.add_user(data)
    session['id'] = new_chef_id
    return redirect("/dashboard")


@app.route('/login', methods=['POST'])
def validate_login():
    data = {"email": request.form["email"]}
    user_in_db = Chef.get_one(data)
    print(user_in_db)
    if not user_in_db:
        flash("Invalid Email/Password", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password", 'login')
        return redirect('/')
    session['id'] = user_in_db.id
    return redirect("/dashboard")


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
