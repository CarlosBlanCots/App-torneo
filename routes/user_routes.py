from flask import Blueprint, render_template, redirect, url_for, flash, session
from flask_login import login_required, current_user
from models import db, User
from forms import EditUserForm

user_bp = Blueprint('user', __name__)

@user_bp.route('/home')
@login_required
def home():
    return render_template('home.html')

@user_bp.route('/perfil')
@login_required
def user_data():
    participantes = User.query.all()
    return render_template('user_data.html', participantes=participantes)

@user_bp.route('/reglas', methods=['GET'])
@login_required
def rules():
    reglas_torneo = session.get('reglas_torneo', [])  # Obtener reglas de la sesión
    return render_template('rules.html', reglas=reglas_torneo)

@user_bp.route('/participants', methods=['GET'])
@login_required
def participants():
    users = User.query.all()  # Obtiene todos los usuarios
    return render_template('participants.html', users=users)
