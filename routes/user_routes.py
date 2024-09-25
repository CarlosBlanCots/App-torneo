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

@user_bp.route('/user/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    # Solo administradores o el propio usuario pueden acceder
    if not (current_user.is_admin or current_user.id == user.id):
        return redirect(url_for('user.home'))

    form = EditUserForm(obj=user)

    # Llenar las opciones de juegos disponibles
    form.games.choices = [(game.id, game.name) for game in Game.query.all()]

    # Preseleccionar los juegos en los que el usuario ya está participando
    if request.method == 'GET':
        form.games.data = [game.id for game in user.games]

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        # Actualizar la contraseña solo si se proporcionó
        if form.password.data:
            user.set_password(form.password.data)

        user.is_admin = form.is_admin.data

        # Actualizar los juegos asignados al usuario
        selected_games = Game.query.filter(Game.id.in_(form.games.data)).all()
        user.games = selected_games

        # Guardar cambios en la base de datos
        db.session.commit()

        flash('¡Información del usuario actualizada!', 'success')
        return redirect(url_for('admin.view_users'))

    return render_template('edit_user.html', form=form, user=user)

@user_bp.route('/perfil')
def user_data():
    participantes = User.query.all()

    return render_template('user_data.html', participantes=participantes)

@user_bp.route('/dashboard')
@login_required
def dashboard():
    participant_data = get_participant_data(current_user.id)
    return render_template('participant_dashboard.html', participant_data=participant_data)


def get_participant_data(participant_id):
    participant = User.query.get(participant_id)
    if participant is None:
        # Manejar el caso donde el participante no existe
        return None

    games = participant.games  # Obtiene los juegos asociados al participante
    return {
        'name': participant.username,  # Nombre del usuario
        'score': participant.score,  # Puntuación del usuario
        'rank': calculate_rank(participant_id),  # Lógica para calcular el rango
        'games': games  # Juegos en los que está inscrito
    }


def calculate_rank(participant_id):
    # Aquí puedes implementar la lógica para calcular el puesto en el ranking
    # Por ejemplo, puedes contar cuántos usuarios tienen más puntuación
    total_users = User.query.filter(User.score > User.query.get(participant_id).score).count()
    return total_users + 1  # El rango es total de usuarios con más puntuación + 1 para el actual


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))