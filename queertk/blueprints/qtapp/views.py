from .qtapp import bp_qtapp
from flask import render_template
from flask_login import login_required

# Import forms
from .forms import ManagePostForm

@bp_qtapp.route('/')
@login_required
def dashboard():
    return render_template('qtapp.html', title = 'QTApp Dashboard')

@bp_qtapp.route('/marketing/posts')
@login_required
def manage_posts():
    form = ManagePostForm()
    return render_template('manage-posts.html', title = 'Manage Posts', form = form)