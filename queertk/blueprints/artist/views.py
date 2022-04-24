from flask import render_template
from .artist import bp_artist

# Import remote models
from queertk.blueprints.common.models import Credit
from queertk.blueprints.production.models import Production

# Import local models
from .models import Artist

# Import database object
from queertk.database import db

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