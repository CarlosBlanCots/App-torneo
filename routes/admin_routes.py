# Rutas para las funciones administrativas de la aplicación

from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required
from models import db
from models.user import User
from models.game import Game
from models.user_game_score import UserGameScore
from forms import EditUserForm, GameForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/games', methods=['GET'])
@login_required
def view_games():
    # Muestra la lista de juegos
    games = Game.query.all()
    return render_template('view_games.html', games=games)

@admin_bp.route('/edit_games', methods=['GET'])
@login_required
def edit_games():
    # Muestra la página para editar juegos
    games = Game.query.all()
    return render_template('edit_games.html', games=games)

@admin_bp.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    # Añade un nuevo juego
    form = GameForm()
    if form.validate_on_submit():
        game_name = form.name.data
        game_rules = form.rules.data

        existing_game = Game.query.filter_by(name=game_name).first()
        if existing_game:
            flash('El juego ya existe. Por favor, elige otro nombre.', 'danger')
            return redirect(url_for('admin.add_game'))

        new_game = Game(name=game_name, rules=game_rules)
        db.session.add(new_game)
        db.session.commit()
        flash('Juego añadido exitosamente.', 'success')
        return redirect(url_for('admin.view_games'))

    return render_template('add_game.html', form=form)

@admin_bp.route('/update_games', methods=['POST'])
@login_required
def update_games():
    # Actualiza los juegos existentes
    games = Game.query.all()
    for game in games:
        game_name = request.form.get(f'game_name_{game.id}')
        game_rules = request.form.get(f'game_rules_{game.id}')
        if game_name and game_rules:
            game.name = game_name
            game.rules = game_rules
            db.session.commit()
    flash('Los juegos han sido actualizados correctamente.', 'success')
    return redirect(url_for('admin.view_games'))

@admin_bp.route('/users')
@login_required
def view_users():
    # Muestra la lista de usuarios
    users = User.query.all()
    return render_template('view_users.html', users=users)

@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    # Edita los detalles de un usuario
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    games = Game.query.all()
    user_game_scores = {score.game_id: score.score for score in user.game_scores}

    form.games.choices = [(game.id, game.name) for game in games]

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data

        selected_game_ids = [int(game_id) for game_id in form.games.data if game_id]
        current_game_ids = list(user_game_scores.keys())

        for game_id in current_game_ids:
            if game_id not in selected_game_ids:
                score = UserGameScore.query.filter_by(user_id=user.id, game_id=game_id).first()
                db.session.delete(score)

        for game_id in selected_game_ids:
            score_value = request.form.get(f'scores_{game_id}', 0)
            if game_id not in current_game_ids:
                new_score = UserGameScore(user_id=user.id, game_id=game_id, score=score_value)
                db.session.add(new_score)
            else:
                existing_score = UserGameScore.query.filter_by(user_id=user.id, game_id=game_id).first()
                if existing_score:
                    existing_score.score = score_value

        db.session.commit()
        flash('Usuario actualizado con éxito.', 'success')
        return redirect(url_for('admin.view_users'))

    user_game_ids = list(user_game_scores.keys())
    form.games.data = user_game_ids

    return render_template('edit_user.html', form=form, user=user, games=games, user_game_scores=user_game_scores)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    # Elimina un usuario
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('¡Usuario eliminado!', 'success')
    return redirect(url_for('admin.view_users'))

@admin_bp.route('/participants', methods=['GET'])
@login_required
def participants():
    # Muestra la lista de participantes
    users = User.query.all()
    return render_template('participants.html', users=users)

def get_current_rules():
    # Obtiene las reglas actuales
    return session.get('reglas_torneo', [])

@admin_bp.route('/modify_rules', methods=['GET', 'POST'])
@login_required
def modify_rules():
    # Modifica las reglas del torneo
    current_rules = get_current_rules()

    if request.method == 'POST':
        new_rules = request.form['rules']
        save_rules(new_rules)
        flash('Reglas actualizadas exitosamente.', 'success')
        return redirect(url_for('user.rules'))

    return render_template('edit_rules.html', current_rules=current_rules)

def save_rules(new_rules):
    # Guarda las reglas en la sesión
    session['reglas_torneo'] = new_rules.splitlines()
