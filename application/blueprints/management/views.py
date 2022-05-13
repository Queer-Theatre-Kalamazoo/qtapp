from . import bp_management
from flask import render_template

# Import forms
from .forms import ManagePostForm


@bp_management.route("/")
def dashboard():
    return render_template("index_management.html", title="Management Dashboard")


@bp_management.route("/marketing/posts")
def manage_posts():
    form = ManagePostForm()
    return render_template("manage-posts.html", title="Manage Posts", form=form)
