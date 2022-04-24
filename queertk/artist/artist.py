from flask import Blueprint, render_template, url_for

# Create blueprint
bp_artist = Blueprint("artists", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/artist") # Create Blueprint

from database import db
from queertk.models import Artist, Credit, Production

@bp_artist.route('/<int:id>')
@bp_artist.route('/<int:id>/<string:name>')
def display_artist(id, **name):
    artist = db.session.query(Artist).filter_by(artist_id = id).one()
    credits = db.session.query(Credit.role, Production.description, Production.production_id, Production.slug, Artist.artist_id).\
        select_from(Credit).\
            join(Production, Production.production_id == Credit.production_id).\
            join(Artist, Artist.artist_id == artist.artist_id).\
                filter(Credit.artist_id == artist.artist_id).\
                    all()

    headshot = url_for('artists.static', filename='images/headshots/connar-klock.jpg')
    
    return render_template('artist.html', 
                            sidebar = True, 
                            artist = artist,
                            title = artist.artist_name,
                            credits = credits,
                            headshot = headshot)