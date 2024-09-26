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

    # Cargar juegos disponibles en la lista de opciones
    form.games.choices = [(game.id, game.name) for game in Game.query.all()]

    # Si el primer usuario se registra, no necesita seleccionar un juego
    if User.query.count() == 0:
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
        # Para usuarios adicionales, la selección de juegos es obligatoria
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
                db.session.commit()

                # Asignar los juegos seleccionados
                selected_games = Game.query.filter(Game.id.in_(form.games.data)).all()
                user.games = selected_games  # Esto actualizará la relación con los juegos

                db.session.commit()
                flash('¡Registro exitoso!', 'success')
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
