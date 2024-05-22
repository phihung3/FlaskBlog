from flask import Blueprint, render_template, redirect, url_for, flash
from flaskblog import db
from flaskblog.models import Post, User
from flask_login import login_required
from flaskblog.admin.decorators import admin_required

admin = Blueprint('admin', __name__, template_folder='templates/admin')

from flask import Blueprint, render_template

admin = Blueprint('admin', __name__, template_folder='templates/admin')

@admin.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@admin.route('/delete_post/<int:post_id>')
@login_required
@admin_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('News item deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # Delete likes and dislikes related to the user
    for post in user.posts:
        post.likes -= post.likes
        post.dislikes -= post.dislikes
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully!', 'success')
    return redirect(url_for('admin.dashboard'))