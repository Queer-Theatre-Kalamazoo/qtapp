from flask import redirect, render_template, request
from . import bp_person
from flask import url_for
from sqlalchemy import select, and_
from application.blueprints.common.schema import Artist, Credit, Production, Person
from application.database import Session


@bp_person.route('/artist/<int:artist_id>')
@bp_person.route('/artist/<string:slug>/<int:artist_id>')
def display_artist(artist_id, slug = None):
    with Session.begin() as session:
        if slug:
            artist = session.execute(select(Artist).where(and_(Artist.artist_id == artist_id, Artist.slug == slug))).scalars().one()
        else:
            artist = session.execute(select(Artist).where(Artist.artist_id == artist_id)).scalars().one()

        credits_query = select(Credit.role, Production.title, Production.production_id, Production.slug, Artist.artist_id).\
            where(Credit.artist_id == artist.artist_id).\
            join(Production, Production.production_id == Credit.production_id).\
            join(Artist, Artist.artist_id == artist.artist_id)
        credits = session.execute(credits_query).all()
        
        return render_template('artist.html',
                            sidebar=True,
                            artist=artist,
                            title=artist.name,
                            credits=credits)


@bp_person.route('/person/<int:person_id>')
@bp_person.route('/person/<string:slug>/<int:person_id>')
def display_person(person_id, slug = None):
    with Session.begin() as session:
        if slug:
            person = session.execute(select(Person).where(and_(Person.person_id == person_id, Person.slug == slug))).scalars().one()
        else:
            person = session.execute(select(Person).where(Person.person_id == person_id)).scalars().one()
        
        return render_template('person.html', sidebar=True, person=person)
