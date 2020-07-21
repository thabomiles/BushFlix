from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for
from flask import Flask, flash, get_flashed_messages
from flask import send_from_directory
from flask_login import current_user
from flask_login import login_required
from flask_login import login_user
from flask_login import logout_user
from werkzeug.urls import url_parse

from app.extensions import db
from app.forms import LoginForm
from app.forms import RegistrationForm
from app.models import User, Films
from config import basedir
import os

server_bp = Blueprint('main', __name__)
uploads = os.path.join(basedir,'app', 'uploads')
tv = os.path.join(basedir,'app', 'tv')

@server_bp.route('/')
def index():
    return render_template("index.html", title='Home Page' )

@server_bp.route('/films/', methods=['GET', 'POST'])
def films():
    films = os.listdir( os.path.join(basedir,'app', 'films') )
    #if request.method == 'POST':
        #return request.form['submit_button']
    #else:
    return render_template("media.html", title='Films', folders=films, media='films' )
    
    
@server_bp.route('/tv')
@server_bp.route('/tv/')
def tv():
    shows = os.listdir( os.path.join(basedir,'app', 'tv') )
    return render_template("media.html", title='TV', folders=shows, media='tv' )

@server_bp.route('/<media>/<show>', methods=['GET', 'POST'])
@login_required
def show(media, show):
    return render_template("show.html", title=show, files = os.listdir(folder), show=show, media=media )
    

@server_bp.route('/flash-test')
def flash():
    flash('You were successfully logged in')
    return render_template("flash.html")

@server_bp.route('/download/<media>/<folder>/<file>')
def downloads(media, folder, file):
    #return str(os.path.join(basedir,'app', folder, file))
    return send_from_directory(directory=os.path.join(basedir,'app', media, folder), filename=file, as_attachment=True)
    #return films
    


@server_bp.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            error = 'Invalid username or password'
            return render_template('login.html', form=form, error=error)

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)

    return render_template('login.html', title='Sign In', form=form)


@server_bp.route('/logout/')
@login_required
def logout():
    logout_user()

    return redirect(url_for('main.index'))


@server_bp.route('/register/', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.login'))

    return render_template('register.html', title='Register', form=form)
