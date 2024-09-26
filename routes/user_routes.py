from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from models.game import Game
from forms import EditUserForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/home')
@login_required
def home():
    return render_template('home.html')

@user_bp.route('/perfil')
def user_data():
    participantes = User.query.all()

    return render_template('user_data.html', participantes=participantes)

@user_bp.route('/reglas')
@login_required
def rules():
    reglas_torneo = [
        "Regla 1: Cada participante debe registrarse antes de la fecha límite.",
        "Regla 2: Se jugarán partidos a eliminación directa.",
        "Regla 3: Las puntuaciones se actualizarán después de cada partida.",
        "Regla 4: Los participantes deben ser respetuosos con los demás.",
    ]
    return render_template('rules.html', reglas=reglas_torneo)

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))