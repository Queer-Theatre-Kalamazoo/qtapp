from flask import redirect, render_template, request
from . import bp_person
from flask import url_for
from sqlalchemy import select
from application.blueprints.common.schema import Artist, Credit, Production, Person
from application.database import Session


@bp_person.route('/artist/<int:artist_id>')
@bp_person.route('/artist/<string:slug>/<int:artist_id>')
def display_artist(artist_id, **slug):
    with Session.begin() as session:
        artist = session.execute(select(Artist).where(Artist.artist_id == artist_id)).scalars().one()
        credits_query = select(Credit.role, Production.title, Production.production_id, Production.slug, Artist.artist_id).\
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
                               title=artist.name,
                               credits=credits,
                               headshot=headshot_filename)


@bp_person.route('/person/<int:person_id>')
def display_person(person_id):
    return render_template('person.html')
