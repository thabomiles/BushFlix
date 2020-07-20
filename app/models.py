from flask_login import UserMixin
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from app.extensions import db
from app.extensions import login


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Films(db.Model):
    film_name = db.Column(db.String(128), primary_key=True)
    year = db.Column(db.Integer)
    imdb_link = db.Column(db.String(128))
    imdb_rating = db.Column(db.Float)
    no_downloads = db.Column(db.Integer)




    def __repr__(self):
        return '<Film {}>'.format(self.film_name)