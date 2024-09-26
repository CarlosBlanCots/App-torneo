from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.game import Game
from models.user_game_score import UserGameScore  # Modelo que relaciona usuarios, juegos y puntuaciones
from forms import EditUserForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
@login_required
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

    # Cargar juegos disponibles
    games = Game.query.all()
    form.game_scores.entries.clear()  # Limpiar entradas previas
    for game in games:
        user_game_score = next((score for score in user.game_scores if score.game_id == game.id), None)
        if user_game_score:
            form.game_scores.append_entry({'game': game.name, 'score': user_game_score.score})
        else:
            form.game_scores.append_entry({'game': game.name, 'score': 0})  # Puntuación por defecto si no hay registro

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data

        if form.password.data:
            user.set_password(form.password.data)

        # Actualizar puntuaciones
        for game_score in form.game_scores.data:
            game_name = game_score['game']
            score = game_score['score']
            game = Game.query.filter_by(name=game_name).first()
            if game:
                # Actualizar o crear el registro de puntuación
                user_game_score = next((score for score in user.game_scores if score.game_id == game.id), None)
                if user_game_score:
                    user_game_score.score = score  # Actualizar la puntuación existente
                else:
                    new_score = UserGameScore(user_id=user.id, game_id=game.id, score=score)
                    db.session.add(new_score)  # Agregar nueva puntuación

        db.session.commit()
        flash('¡Información del usuario actualizada!', 'success')
        return redirect(url_for('admin.view_users'))

    return render_template('edit_user.html', form=form, user=user)

@admin_bp.route('/users/update_score/<int:user_id>', methods=['POST'])
@login_required
def update_score(user_id):
    user = User.query.get_or_404(user_id)
    new_score = request.form.get('score', type=int)

    if new_score is not None:
        # Lógica para actualizar la puntuación dinámica según el juego
        game_id = request.form.get('game_id', type=int)
        user_game_score = UserGameScore.query.filter_by(user_id=user.id, game_id=game_id).first()

        if user_game_score:
            user_game_score.score = new_score
            db.session.commit()
            flash('Puntuación actualizada correctamente.', 'success')
        else:
            flash('Error al encontrar la puntuación.', 'danger')
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
