from flask import Blueprint, render_template

# Create blueprint
bp_artist = Blueprint("artists", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/artist") # Create Blueprint

from database import db
from queertk.models import Artist

@bp_artist.route('/<int:id>')
@bp_artist.route('/<int:id>/<string:name>')
def display_artist(id, **name):
    artist = db.session.query(Artist).filter_by(artist_id = id).one()
    name = artist.artist_name
    
    return render_template('artist.html', 
                            sidebar = True, 
                            artist = artist)