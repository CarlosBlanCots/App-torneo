from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from models import db
from models.user import User
from models.game import Game
from models.user_game_score import UserGameScore  # Modelo que relaciona usuarios, juegos y puntuaciones
from forms import EditUserForm, GameForm

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/games', methods=['GET'])
@login_required
def view_games():
    games = Game.query.all()
    return render_template('view_games.html', games=games)

@admin_bp.route('/edit_games', methods=['GET'])
@login_required
def edit_games():
    games = Game.query.all()
    return render_template('edit_games.html', games=games)

@admin_bp.route('/add_game', methods=['GET', 'POST'])
@login_required
def add_game():
    form = GameForm()
    if form.validate_on_submit():
        game_name = form.name.data
        game_rules = form.rules.data

        # Verificar si el juego ya existe
        existing_game = Game.query.filter_by(name=game_name).first()
        if existing_game:
            flash('El juego ya existe. Por favor, elige otro nombre.', 'danger')
            return redirect(url_for('admin.add_game'))

        # Crear y agregar el nuevo juego
        new_game = Game(name=game_name, rules=game_rules)
        db.session.add(new_game)
        db.session.commit()
        flash('Juego añadido exitosamente.', 'success')
        return redirect(url_for('admin.view_games'))

    return render_template('add_game.html', form=form)

@admin_bp.route('/update_games', methods=['POST'])
@login_required
def update_games():
    # Obtener todos los juegos
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
    users = User.query.all()
    return render_template('view_users.html', users=users)


@admin_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    form = EditUserForm(obj=user)

    # Cargar los juegos disponibles y establecer las opciones en el formulario
    games = Game.query.all()
    form.games.choices = [(game.id, game.name) for game in games]  # Llenar choices

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data

        # Actualiza la relación de juegos
        selected_game_ids = [int(game_id) for game_id in request.form.getlist('games')]  # Convertir a enteros
        current_game_ids = [score.game_id for score in user.game_scores]  # Obtiene los IDs de los juegos actuales

        # Eliminar juegos no seleccionados
        for game_id in current_game_ids:
            if game_id not in selected_game_ids:
                score = UserGameScore.query.filter_by(user_id=user.id, game_id=game_id).first()
                db.session.delete(score)

        # Agregar nuevos juegos
        for game_id in selected_game_ids:
            if game_id not in current_game_ids:
                new_score = UserGameScore(user_id=user.id, game_id=game_id)
                db.session.add(new_score)

        db.session.commit()
        flash('Usuario actualizado con éxito.', 'success')
        return redirect(url_for('admin.view_users'))
    else:
        print(form.errors)

    user_game_ids = [score.game_id for score in user.game_scores]
    return render_template('edit_user.html', form=form, user=user, games=games, user_game_ids=user_game_ids)



@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('¡Usuario eliminado!', 'success')
    return redirect(url_for('admin.view_users'))


@admin_bp.route('/participants', methods=['GET'])
@login_required
def participants():
    users = User.query.all()  # Obtener todos los usuarios
    return render_template('participants.html', users=users)

def get_current_rules():
    # Obtener las reglas de la sesión o devolver una lista vacía si no existen
    return session.get('reglas_torneo', [])


@admin_bp.route('/modify_rules', methods=['GET', 'POST'])
@login_required
def modify_rules():
    # Cargar las reglas actuales
    current_rules = get_current_rules()

    if request.method == 'POST':
        new_rules = request.form['rules']
        save_rules(new_rules)  # Guardar las nuevas reglas en la sesión
        flash('Reglas actualizadas exitosamente.', 'success')
        return redirect(url_for('user.rules'))

    return render_template('edit_rules.html', current_rules=current_rules)


def save_rules(new_rules):
    # Guardar las reglas en la sesión
    session['reglas_torneo'] = new_rules.splitlines()  # Separar las reglas por líneas
