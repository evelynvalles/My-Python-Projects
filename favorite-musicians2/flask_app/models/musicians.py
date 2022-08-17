from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import users
from flask import flash
DATABASE = "musicians2"

class Musician:
    
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.artist_name = data['artist_name']
        self.genre = data['genre']
        self.favorite_song = data['favorite_song']
        self.birthday = data['birthday']
        self.hometown = data['hometown']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save(cls,data):
        query= "INSERT INTO musicians (first_name, last_name, artist_name, genre, favorite_song, birthday, hometown, user_id) VALUES (%(first_name)s,%(last_name)s,%(artist_name)s, %(genre)s, %(favorite_song)s, %(birthday)s, %(hometown)s, %(user_id)s);"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def update(cls,data):
        query = "UPDATE musicians SET first_name = %(first_name)s, last_name = %(last_name)s, artist_name = %(artist_name)s, genre = %(genre)s, favorite_song = %(favorite_song)s, birthday = %(birthday)s, hometown = %(hometown)s WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM musicians WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM musicians JOIN users ON users.id = musicians.user_id;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_musicians = []
            for row in results:
                this_musician = Musician(row)
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'first_name': row['users.first_name'],
                    'last_name': row['users.last_name'],
                    'created_at':row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                this_user = users.User(user_data)
                this_musician.person = this_user
                all_musicians.append(this_musician)
            return all_musicians
        return results

    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM musicians JOIN users ON users.id = musicians.user_id WHERE musicians.id = %(id)s"
        result = connectToMySQL(DATABASE).query_db(query,data)
        row = result[0]
        print(row)
        this_musician = Musician(row)
        user_data = {
            **row,
            'id': row['users.id'],
            'first_name': row['users.first_name'],
            'last_name': row['users.last_name'],
            'created_at': row['users.created_at'],
            "updated_at": row['users.updated_at']
        }
        person = users.User(user_data)
        this_musician.person = person
        return this_musician

    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['first_name']) < 3:
            is_valid = False
            flash("First name must be at least 3 characters long", "m_err_first_name")
        if len(form_data['last_name']) < 3:
            is_valid = False
            flash("Last name must be at least 3 characters long", "m_err_last_name")
        if len(form_data['artist_name']) < 3:
            is_valid= False
            flash("Artist Name must be at least 3 characters long", "err_artist_name")
        if "genre" not in form_data:
            is_valid = False
            flash("Genre field must be selected", "err_genre")
        if len(form_data['favorite_song']) < 3:
            is_valid = False
            flash("Favorite song must be at least 3 characters long", "err_favorite_song")
        if len(form_data['birthday']) < 1:
            is_valid = False
            flash("Birthday field is required", "err_birthday")
        if len(form_data['hometown']) < 3:
            is_valid = False
            flash("Hometown must be at least 3 characters long", "err_hometown")
        return is_valid