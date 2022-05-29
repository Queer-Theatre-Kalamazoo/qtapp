from . import bp_management
from flask import render_template, redirect, url_for

# Import forms
from .forms import PostForm

from application.database import Session
from application.blueprints.common.schema import Post
import datetime

from sqlalchemy import select

@bp_management.route("/")
def dashboard():
    return render_template("index_management.html", title="Management Dashboard")


@bp_management.route("/post/new", methods=['GET', 'POST'])
def post_new():
    form = PostForm()

    if form.validate_on_submit():
        with Session.begin() as session:
            print(f"Posted - Type: {form.type.data}, Title: {form.title.data}, Author: {form.author.data.artist_id}")
            post = Post(author_id=form.author.data.artist_id, type=form.type.data, title=form.title.data, subtitle=form.subtitle.data, content = form.content.data, create_date = datetime.datetime.utcnow(), last_updated = datetime.datetime.utcnow())
            session.add(post)
            # Flush and refresh seem to be required to retrieve the post_id after it's been added
            session.flush()
            session.refresh(post, attribute_names=['post_id'])
            print(post.post_id)
            return redirect(url_for('bp_management.post_update', post_id=post.post_id))

    return render_template("manage-post.html", title="New Post", form=form)


@bp_management.route("/post/update/<int:post_id>", methods=['GET', 'POST'])
def post_update(post_id):
    with Session.begin() as session:
        post = session.execute(select(Post).where(Post.post_id == post_id)).scalars().one()
        form = PostForm(obj=post)

        if form.validate_on_submit():
            form.populate_obj(post)
            session.add(post)
            return redirect(url_for('bp_management.post_update', post_id=post.post_id))

    return render_template('manage-post.html', title="Update Post", form=form)
