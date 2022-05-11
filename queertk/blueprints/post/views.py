from flask import render_template

# Import remote models
from queertk.blueprints.artist.models import Artist
from queertk.blueprints.post.models import Post

# Import local models
from .post import bp_post

# Import database object
from queertk.database import Session

@bp_post.route('/<int:post_id>')
def display_post(post_id):
    post = Session.begin().query(Post).filter_by(post_id = post_id).one()
    author = Session.begin().query(Artist).filter_by(artist_id = post.author_id).one()
    return render_template('post.html', post = post, author = author)