from flask import render_template

# Import remote models
from application.blueprints.common.schema import Artist, Post

# Import local models
from . import bp_post

# Import database object
from application.database import Session
from sqlalchemy import select


@bp_post.route("/<int:post_id>")
def display_post(post_id):
    with Session.begin() as session:
        post = (
            session.execute(select(Post).where(Post.post_id == post_id)).scalars().one()
        )
        author = (
            session.execute(select(Artist).where(Artist.artist_id == post.author_id))
            .scalars()
            .one()
        )
        return render_template("post.html", post=post, author=author)
