from math import prod
from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from flask import current_app
from application.database import Session
from application.blueprints.common.schema import Season, Production, Post, Person, Relationship, Artist, Credit, Performance
from sqlalchemy import select, and_, func


@current_app.route('/')
@register_breadcrumb(current_app, '.', 'Home')
def home():
    return render_template('index.html', title='Home')


@current_app.route('/events')
@register_breadcrumb(current_app, '.events', 'Events')
def events():
    with Session.begin() as session:
        query_productions = select(
                        Production.description.label('prod_desc'),
                        Production.slug,
                        Production.poster,
                        Production.production_id).\
                            where(Season.season_id == 1)
        productions = session.execute(query_productions).all()

        prod_ids = select(Production.production_id).where(Season.season_id == 1).subquery()

        query_directors = select(
                            Credit.credit_name,
                            Credit.artist_id,
                            Credit.production_id
                        ).where(and_(Credit.role == "Director", Credit.production_id.in_(prod_ids))).subquery()
        directors = session.query(query_directors)

        query_performances = select(
                                Performance.production_id,
                                func.min(Performance.datetime).label('open_date'),
                                func.max(Performance.datetime).label('close_date')
                            ).where(Performance.production_id.in_(prod_ids)).group_by(Performance.production_id).subquery()
        performances = session.query(query_performances)

        
        return render_template('events.html', title='Events', productions=productions, performances=performances, directors=directors)


@current_app.route('/news')
@register_breadcrumb(current_app, '.news', 'News')
def news():
    with Session.begin() as session:
        # So I guess you use just .all() if there's a join, or .scalars().all() otherwise?
        posts = session.execute(select(Post.title, Post.subtitle, Post.content, Post.post_id, Post.create_date, Artist.artist_name.label('name'), Artist.slug.label('artist_slug'), Artist.artist_id).where(Post.type == "News").join(Artist, Post.author_id == Artist.artist_id).order_by(Post.create_date.desc())).all()
        return render_template('news.html', title='News', posts=posts)


@current_app.route('/about')
@register_breadcrumb(current_app, '.about', 'About Us')
def about():
    with Session.begin() as session:
        with Session.begin() as session:
            staff = session.execute(
                select(Person.name, Person.person_id, Person.artist_id, Relationship.title).select_from(Person).where(and_(Relationship.type == "Staff", Relationship.show_online == True)).join(Relationship, Relationship.person_id == Person.person_id)).all()
            board = session.execute(
                select(Person.name, Person.person_id, Person.artist_id, Relationship.title).select_from(Person).where(and_(Relationship.type == "Board", Relationship.show_online == True)).join(Relationship, Relationship.person_id == Person.person_id)).all()
            
            def get_artist_headshot(artist_id):
                artist = session.execute(
                                    select(Artist.headshot).where(Artist.artist_id == artist_id)
                                    ).one()
                return artist.headshot
        return render_template('about.html', title="About Us", staff=staff, board=board, get_headshot=get_artist_headshot)