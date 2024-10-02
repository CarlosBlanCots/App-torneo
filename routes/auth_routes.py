# auth_routes.py: Define las rutas de autenticación, registro y gestión de usuarios.

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models import db
from models.user import User
from models.game import Game
from models.user_game_score import UserGameScore
from forms import AdminRegistrationForm, RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Maneja el registro de nuevos usuarios, con la posibilidad de crear un administrador si es el primer registro.
    if User.query.count() == 0:
        form = AdminRegistrationForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data
            )
            user.set_password(form.password.data)
            user.is_admin = True  # Hacerlo administrador
            db.session.add(user)
            db.session.commit()
            flash('¡Registro exitoso! Eres el administrador del torneo.', 'success')
            return redirect(url_for('auth.login'))
    else:
        form = RegistrationForm()
        # Cargar juegos disponibles en la lista de opciones
        form.games.choices = [(game.id, game.name) for game in Game.query.all()]
        if form.validate_on_submit():
            if not form.games.data:
                form.games.errors.append("Debes seleccionar al menos un juego para registrarte.")
            else:
                user = User(
                    username=form.username.data,
                    email=form.email.data
                )
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()  # Aquí ya se ha añadido el usuario

                # Asignar los juegos seleccionados y crear entradas en user_game_scores
                for game_id in form.games.data:
                    new_score_entry = UserGameScore(user_id=user.id, game_id=game_id, score=0)
                    db.session.add(new_score_entry)  # Añadir la nueva entrada

                db.session.commit()  # Guardar cambios en la base de datos
                flash('¡Registro exitoso!', 'success')
                return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    # Maneja el inicio de sesión de usuarios existentes.
    if current_user.is_authenticated:
        return redirect(url_for('user.home'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('¡Has iniciado sesión exitosamente!', 'success')
            return redirect(url_for('user.home'))
        else:
            flash('Email o contraseña incorrectos.', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    # Maneja la acción de cierre de sesión.
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))
