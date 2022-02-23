from flask_app.models.ninja import Ninja
from flask_app.config.mysqlconnection import MySQLConnection, connectToMySQL

class Dojo:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.ninjas = []

    @classmethod
    def get_all_dojos(cls):
        query = "SELECT * FROM dojos;"
        results = connectToMySQL('dojos_and_ninjas_schemas').query_db(query)
        dojos = []
        for item in results:
            dojos.append(Dojo(item))
        return dojos

    @classmethod
    def create_dojo(cls, data):
        query = "INSERT INTO dojos (name, created_at) VALUES (%(name)s, NOW());"
        return connectToMySQL('dojos_and_ninjas_schemas').query_db(query, data)

    @classmethod
    def show_dojo(cls, data):
        query = "SELECT * FROM dojos JOIN ninjas ON ninjas.dojo_id = dojos.id WHERE dojos.id = %(id)s"
        result = connectToMySQL('dojos_and_ninjas_schemas').query_db(query, data)

        dojo = cls(result[0])
        for row_fromdb in result:
            ninja_data = {
                'id': row_fromdb['ninjas.id'],
                'first_name': row_fromdb['first_name'],
                'last_name': row_fromdb['last_name'],
                'age': row_fromdb['age'],
                'created_at': row_fromdb['ninjas.created_at'],
                'updated_at': row_fromdb['ninjas.updated_at'],
            }
            dojo.ninjas.append(Ninja( ninja_data ) )
        return dojo