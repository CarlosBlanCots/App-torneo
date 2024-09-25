from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from models.user import User
from models import db
from models.game import Game
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    form.games.choices = [(game.id, game.name) for game in Game.query.all()]

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        selected_game_ids = form.games.data

        first_user = User.query.first()
        is_admin = first_user is None

        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.is_admin = is_admin

        selected_games = Game.query.filter(Game.id.in_(selected_game_ids)).all()
        new_user.games = selected_games

        db.session.add(new_user)
        db.session.commit()

        flash('¡Te has registrado exitosamente!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            session['user_role'] = 'admin' if user.is_admin else 'participant'  # Almacena el rol en la sesión
            flash('¡Has iniciado sesión exitosamente!', 'success')
            return redirect(url_for('user.home'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)



@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))