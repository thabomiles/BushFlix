import os
from app.models import *

def write_films( path ):
    for i in os.listdir( path ):
        u = Films(film_name=i)
        db.session.add(u)
        db.session.commit()


def traversal( directory ):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            print(filename)
