from flask import render_template
from .artist import bp_artist
from database import db

from .models import Artist
from queertk.models import Credit, Production

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

    # If artist has a headshot, set variable to be passed - if not, set to None to avoid passing a nonexistant variable
    if artist.headshot:
        headshot_filename = 'images/headshots/' + artist.headshot
    else:
        headshot_filename = None
    
    return render_template('artist.html', 
                            sidebar = True, 
                            artist = artist,
                            title = artist.artist_name,
                            credits = credits,
                            headshot = headshot_filename)