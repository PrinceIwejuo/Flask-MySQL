from flask_app import app

from flask import render_template, redirect, request, session, flash

from flask_app.models.user import User

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index():

    return render_template('index.html')

@app.route('/users/register', methods=['POST'])
def register_user():

    if not User.validate_new_user(request.form):
        print("validation failed")
        return redirect('/')

    else:
        print("validation worked")
        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }
        print(data)
        User.create_new_user(data )
        flash("User is now registered; log in with that account")
        return redirect('/')

@app.route('/users/login', methods=['POST'])
def login_user():
    
    user = User.get_user_by_email(request.form)

    if not user:
        flash("This email does not exist.")
        return redirect('/')

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password is incorrect")
        return redirect('/')

    session['user_id'] = user.id
    session['user_email'] = user.email
    session['user_first_name'] = user.first_name

    return redirect('/recipes')


@app.route('/users/logout')
def logout():
    session.clear()
    flash("You've logged out, see you next time!")
    return redirect('/')
