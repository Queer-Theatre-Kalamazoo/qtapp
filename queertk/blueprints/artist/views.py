from flask import render_template
from .artist import bp_artist
from sqlalchemy import select
from sqlalchemy.orm import aliased

# Import remote models
from queertk.blueprints.common.models import Credit
from queertk.blueprints.production.models import Production

# Import local models
from .models import Artist

# Import database object
from queertk.database import Session


@bp_artist.route('/<int:id>')
@bp_artist.route('/<int:id>/<string:name>')
def display_artist(id, **name):

    with Session.begin() as session:
        artist = session.execute(select(Artist).where(Artist.artist_id == id)).scalars().one()
        credits_query = select(Credit.role, Production.description, Production.production_id, Production.slug, Artist.artist_id).\
            where(Credit.artist_id == artist.artist_id).\
            join(Production, Production.production_id == Credit.production_id).\
            join(Artist, Artist.artist_id == artist.artist_id)
        credits = session.execute(credits_query).all()

        # If artist has a headshot, set variable to be passed - if not, set to None to avoid passing a nonexistant variable
        if artist.headshot:
            headshot_filename = 'images/headshots/' + artist.headshot
        else:
            headshot_filename = None

        return render_template('artist.html',
                               sidebar=True,
                               artist=artist,
                               title=artist.artist_name,
                               credits=credits,
                               headshot=headshot_filename)
