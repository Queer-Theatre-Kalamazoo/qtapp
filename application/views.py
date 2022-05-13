from flask import render_template
from flask_breadcrumbs import register_breadcrumb
from application import app
from application.database import Session
from application.blueprints.common.models import Season
from application.blueprints.production.models import Production
from application.blueprints.post.models import Post
from sqlalchemy import select

@app.route('/')
@register_breadcrumb(app, '.', 'Home')
def home():
    return render_template('index.html', title = 'Home')

@app.route('/events')
@register_breadcrumb(app, '.', 'Events')
def events():
    with Session.begin() as session:
        productions = session.execute(select(Production.description.label('prod_desc'), Production.slug, Production.production_id, Season.description.label(
            "season_desc")).where(Season.season_id == 1).join(Season, Season.season_id == Production.season_id)).all()
        return render_template('events.html', title = 'Events', productions = productions)

@app.route('/news')
@register_breadcrumb(app, '.', 'News')
def news():
    with Session.begin() as session:
        posts = session.execute(select(Post)).scalars().all()
        return render_template('news.html', title = 'News', posts = posts)