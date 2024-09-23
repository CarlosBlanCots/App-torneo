from flask import Blueprint, render_template, redirect, url_for, flash, request
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


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))