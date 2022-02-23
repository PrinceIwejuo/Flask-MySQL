from flask_app import app
from flask import render_template, redirect, request
import flask_app
from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models.dojo import Dojo

@app.route('/')
def index():
    dojos = Dojo.get_all_dojos()

    return render_template('dojo.html', dojos = dojos)

@app.route('/dojos', methods = ['POST'])
def create_dojo():
    data = {
        'name': request.form['name']
    }
    Dojo.create_dojo(data)
    return redirect('/')

@app.route('/dojos/<int:id>')
def show_dojo(id):
    data = {
        'id' : id
    }
    dojos1 = Dojo.show_dojo(data)
    return render_template('dojo_show.html', dojo = dojos1)