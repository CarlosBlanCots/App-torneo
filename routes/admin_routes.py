from flask import Blueprint, render_template, redirect, url_for, flash
from models import db
from models.user import User

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/users')
def view_users():
    users = User.query.all()
    return render_template('view_users.html', users=users)

@admin_bp.route('/admin/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash('¡Usuario eliminado!')
    return redirect(url_for('admin.view_users'))
