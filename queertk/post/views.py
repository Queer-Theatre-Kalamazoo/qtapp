from flask import render_template

# Import remote models
from queertk.artist.models import Artist
from queertk.post.models import Post

# Import local models
from .post import bp_post

# Import database object
from database import db

@bp_post.route('/<int:post_id>')
def display_post(post_id):
    post = db.session.query(Post).filter_by(post_id = post_id).one()
    author = db.session.query(Artist).filter_by(artist_id = post.author_id).one()
    return render_template('post.html', post = post, author = author)