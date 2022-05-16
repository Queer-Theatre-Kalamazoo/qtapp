from flask import render_template, url_for, request
from flask_breadcrumbs import register_breadcrumb

# Import remote models
from application.blueprints.common.schema import Artist, Post

# Import local models
from . import bp_post

# Import database object
from application.database import Session
from sqlalchemy import select, and_


@bp_post.route("/<string:category>/<int:post_id>")
def display_post(category, post_id):
    category = category.lower()
    with Session.begin() as session:
        post = session.execute(select(Post.post_id, Post.category, Post.title, Post.subtitle, Post.content, Post.author_id).where(Post.post_id == post_id)).one()
        author = (
            session.execute(select(Artist).where(Artist.artist_id == post.author_id)).scalars().one()
        )
        return render_template("post.html", post=post, author=author, title=post.title)
