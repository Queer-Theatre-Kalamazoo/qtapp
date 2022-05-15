from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from flask import current_app
from application.database import Session
from application.blueprints.common.schema import Season, Production, Post, Person, Relationship, Artist
from sqlalchemy import select, and_


@current_app.route('/')
@register_breadcrumb(current_app, '.', 'Home')
def home():
    return render_template('index.html', title='Home')


@current_app.route('/events')
@register_breadcrumb(current_app, '.', 'Events')
def events():
    with Session.begin() as session:
        productions = session.execute(select(Production.description.label('prod_desc'), Production.slug, Production.production_id, Season.description.label(
            "season_desc")).where(Season.season_id == 1).join(Season, Season.season_id == Production.season_id)).all()
        return render_template('events.html', title='Events', productions=productions)


@current_app.route('/news')
@register_breadcrumb(current_app, '.', 'News')
def news():
    with Session.begin() as session:
        # So I guess you use just .all() if there's a join, or .scalars().all() otherwise?
        posts = session.execute(select(Post.title, Post.subtitle, Post.content, Post.post_id, Post.create_date, Artist.artist_name.label('name'), Artist.slug.label('artist_slug'), Artist.artist_id).where(Post.type == "News").join(Artist, Post.author_id == Artist.artist_id).order_by(Post.create_date.desc())).all()
        return render_template('news.html', title='News', posts=posts)


@current_app.route('/about')
@register_breadcrumb(current_app, '.', 'About Us')
def about():
    with Session.begin() as session:
        with Session.begin() as session:
            staff = session.execute(
                select(Person.name, Relationship.title).select_from(Person).where(and_(Relationship.type == "Staff", Relationship.show_online == True)).join(Relationship, Relationship.person_id == Person.person_id)).all()
            board = session.execute(
                select(Person.name, Relationship.title).select_from(Person).where(and_(Relationship.type == "Board", Relationship.show_online == True)).join(Relationship, Relationship.person_id == Person.person_id)).all()
        return render_template('about.html', title="About Us", staff=staff, board=board)