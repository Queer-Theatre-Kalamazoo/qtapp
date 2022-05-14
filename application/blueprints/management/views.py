from . import bp_management
from flask import render_template, redirect, url_for

# Import forms
from .forms import UpdatePostForm

from application.database import Session
from application.blueprints.common.schema import Post
import datetime


@bp_management.route("/")
def dashboard():
    return render_template("index_management.html", title="Management Dashboard")


@bp_management.route("/update-post", methods=['GET', 'POST'])
def update_post():
    form = UpdatePostForm()

    if UpdatePostForm().validate_on_submit():
        with Session.begin() as session:
            print(f"Posted - Type: {form.type.data}, Title: {form.title.data}, Author: {form.author.data.artist_id}")
            post = Post(author_id = form.author.data.artist_id, type = form.type.data, title = form.title.data, subtitle = form.subtitle.data, content = form.content.data, create_date = datetime.datetime.utcnow(), last_updated = datetime.datetime.utcnow())
            session.add(post)
            return redirect(url_for('bp_management.update_post'))

    return render_template("update-post.html", title="Update Post", form=form)
