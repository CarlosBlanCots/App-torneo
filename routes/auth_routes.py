from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models.user import User
from models import db  # Asegúrate de importar 'db' desde models
from forms import RegistrationForm, LoginForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        # Verificar si ya hay usuarios en la base de datos
        first_user = User.query.first()
        is_admin = first_user is None

        # Crear un nuevo usuario
        new_user = User(username=username, email=email)
        new_user.set_password(password)
        new_user.is_admin = is_admin

        # Añadir el nuevo usuario a la base de datos
        db.session.add(new_user)
        db.session.commit()

        flash('¡Te has registrado exitosamente!', 'success')
        return redirect(url_for('auth.login'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('¡Inicio de sesión exitoso!', 'success')
            return redirect(url_for('user.home'))  # Redirige a la página de inicio o dashboard
        flash('Credenciales incorrectas. Inténtalo de nuevo.', 'danger')

    return render_template('login.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('¡Has cerrado sesión!', 'info')
    return redirect(url_for('auth.login'))
