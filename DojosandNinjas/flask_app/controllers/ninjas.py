
from flask_app import app
from flask import render_template, redirect, request
import flask_app
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.dojo import Dojo
from flask_app.models.ninja import Ninja

@app.route('/ninjas', methods = ['POST'])
def create_ninja():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'age': request.form['age'],
        'dojo_id': request.form['dojo_id']
    }
    Ninja.create_ninja(data)
    return redirect(f"/dojos/{request.form['dojo_id']}")

@app.route('/ninjas')
def created_ninja():

    return render_template('new_ninja.html', dojos = Dojo.get_all_dojos())
