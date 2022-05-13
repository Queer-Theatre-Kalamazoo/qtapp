from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from flask import current_app
from application.database import Session
from application.blueprints.common.schema import Season, Production, Post
from sqlalchemy import select

@current_app.route('/')
@register_breadcrumb(current_app, '.', 'Home')
def home():
    return render_template('index.html', title = 'Home')

@current_app.route('/events')
@register_breadcrumb(current_app, '.', 'Events')
def events():
    with Session.begin() as session:
        productions = session.execute(select(Production.description.label('prod_desc'), Production.slug, Production.production_id, Season.description.label(
            "season_desc")).where(Season.season_id == 1).join(Season, Season.season_id == Production.season_id)).all()
        return render_template('events.html', title = 'Events', productions = productions)

@current_app.route('/news')
@register_breadcrumb(current_app, '.', 'News')
def news():
    with Session.begin() as session:
        posts = session.execute(select(Post)).scalars().all()
        return render_template('news.html', title = 'News', posts = posts)