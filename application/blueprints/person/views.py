from flask import redirect, render_template, request
from . import bp_person
from flask import url_for
from sqlalchemy import select
from application.blueprints.common.schema import Artist, Credit, Production, Person
from application.database import Session
from flask_breadcrumbs import register_breadcrumb, default_breadcrumb_root


# Get variable values for display_artist() breadcrumbs
def bc_view_artist(*args, **kwargs):
    with Session.begin() as session:
        artist_id = request.view_args['artist_id']
        artist_query = select(Artist.artist_id, Artist.name).where(Artist.artist_id == artist_id)
        artist = session.execute(artist_query).one()
        return [{'text': artist.name, 'url': Artist.get_url(artist)}]


@bp_person.route('/a/<int:artist_id>')
@bp_person.route('/a/<int:artist_id>/<string:slug>')
@register_breadcrumb(bp_person, '.artist', '', dynamic_list_constructor=bc_view_artist)
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


# Get variable values for display_person() breadcrumbs
def bc_view_person(*args, **kwargs):
    with Session.begin() as session:
        person_id = request.view_args['person_id']
        person_query = select(Person.person_id, Person.name).where(Person.person_id == person_id)
        person = session.execute(person_query).one()
        return [{'text': person.name, 'url': Person.get_url(person)}]


@bp_person.route('/<int:person_id>')
@register_breadcrumb(bp_person, '.person', '', dynamic_list_constructor=bc_view_person)
def display_person(person_id):
    return render_template('person.html')


@bp_person.route('/')
@register_breadcrumb(bp_person, '.', 'Person')
def person_index():
    return redirect(url_for('home'))