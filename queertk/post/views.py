from flask import render_template
from .post import bp_post
from database import db
from queertk.models import Artist
from queertk.post.models import Post

@bp_post.route('/<int:post_id>')
def display_post(post_id):
    post = db.session.query(Post).filter_by(post_id = post_id).one()
    author = db.session.query(Artist).filter_by(artist_id = post.author_id).one()
    return render_template('post.html', post = post, author = author)