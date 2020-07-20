import os
basedir = os.path.abspath(os.path.dirname(__file__))
file_path = os.path.abspath(os.getcwd())+"\app.db"

class BaseConfig:
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ['SECRET_KEY'] 
