
from flask import, render_template, redirect, request

from flask_app import app
from mysqlconnnection import connectToMySQL

from user import User




@app.route('/')
def index():
    users = User.get_all_users()

    return render_template('Read(All).html', users = users)

@app.route('/users/new')
def new_user():

    return render_template('Create.html')

@app.route('/users/create', methods = ['POST'])
def create_user():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    User.create_user(data)
    return redirect('/')

@app.route('/users/<int:id>')
def show_user(id):
    data = {
        'id': id
    }
    user1 = User.show_user(data) 
    return render_template('Read(One).html', user = user1 )

@app.route('/users/<int:id>/delete')
def delete_user(id):
    data = {
        'id': id
    }
    User.delete_user(data)
    return redirect('/')


@app.route('/users/<int:id>/edit')
def edit_user(id):
    data = {
        'id': id
    }
    user = User.show_user(data)
    return render_template('Edit.html', user = user)


@app.route('/users/edit', methods = ['POST'])
def processedit_user():
    
    User.update_user(request.form)
    return redirect('/')

if __name__=="__main__":
    app.run(debug=True)