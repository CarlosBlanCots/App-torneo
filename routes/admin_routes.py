from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required
from models import db
from models.user import User  # Asegúrate de importar el modelo User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users')
def view_users():
    users = User.query.all()  # Es más común usar User.query.all() en lugar de db.session.query(User).all()
    return render_template('view_users.html', users=users)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)  # Aquí también puedes usar User.query.get_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('¡Usuario eliminado!')
    return redirect(url_for('admin.view_users'))

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    # Aquí puedes obtener datos de los participantes y juegos, por ejemplo:
    # participants = get_all_participants()
    # games = get_all_games()
    return render_template('admin_dashboard.html', participants=[], games=[])