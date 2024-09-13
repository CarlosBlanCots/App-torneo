from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db
from models.user import User
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
    if not (current_user.is_admin or current_user.id == user.id):
        return redirect(url_for('user.home'))

    form = EditUserForm(obj=user)
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.password.data:
            user.set_password(form.password.data)
        user.is_admin = form.is_admin.data
        db.session.commit()
        flash('¡Información del usuario actualizada!', 'success')
        return redirect(url_for('admin.view_users'))

    return render_template('edit_user.html', form=form, user=user)
