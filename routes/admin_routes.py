from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.user import User  # Asegúrate de importar el modelo User
from models.game import Game  # Asegúrate de importar el modelo Game
from forms import EditUserForm  # Asegúrate de importar el formulario EditUserForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@admin_bp.route('/edit/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)

    if not current_user.is_admin:
        return redirect(url_for('user.home'))

    form = EditUserForm(obj=user)

    form.games.choices = [(game.id, game.name) for game in Game.query.all()]

    if request.method == 'GET':
        # Cargar los juegos del usuario y las puntuaciones
        form.games.data = [game.id for game in user.games]
        form.pacman_score.data = user.pacman_score  # Asegúrate de que estos campos existan
        form.tetris_score.data = user.tetris_score

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        if form.password.data:
            user.set_password(form.password.data)

        user.is_admin = form.is_admin.data

        # Actualizar puntuaciones
        user.pacman_score = form.pacman_score.data
        user.tetris_score = form.tetris_score.data

        selected_games = Game.query.filter(Game.id.in_(form.games.data)).all()
        user.games = selected_games

        db.session.commit()

        flash('¡Información del usuario actualizada!', 'success')
        return redirect(url_for('admin.view_users'))

    return render_template('edit_user.html', form=form, user=user)

@admin_bp.route('/users/update_score/<int:user_id>', methods=['POST'])
@login_required
def update_score(user_id):
    user = User.query.get_or_404(user_id)
    new_score = request.form.get('score', type=int)

    # Asegúrate de actualizar la puntuación correcta, ¿debería ser pacman_score o tetris_score?
    if new_score is not None:
        user.pacman_score = new_score  # Cambiar esto si es necesario
        db.session.commit()
        flash('Puntuación actualizada correctamente.', 'success')
    else:
        flash('Error al actualizar la puntuación.', 'danger')

    return redirect(url_for('admin.view_users'))

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('¡Usuario eliminado!', 'success')
    return redirect(url_for('admin.view_users'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_dashboard.html', participants=[], games=[])
