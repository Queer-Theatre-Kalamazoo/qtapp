from flask import render_template
from queertk import app
from queertk.database import Session
from queertk.blueprints.common.models import Season
from queertk.blueprints.production.models import Production
from queertk.blueprints.post.models import Post
from sqlalchemy import select

@app.route('/')
def home():
    return render_template('index.html', title = 'Home')

@app.route('/events')
def events():
    with Session.begin() as session:
        productions = session.execute(select(Production.description.label('prod_desc'), Production.slug, Production.production_id, Season.description.label(
            "season_desc")).where(Season.season_id == 1).join(Season, Season.season_id == Production.season_id)).all()
        return render_template('events.html', title = 'Events', productions = productions)

@app.route('/news')
def news():
    with Session.begin() as session:
        posts = session.execute(select(Post)).scalars().all()
        return render_template('news.html', title = 'News', posts = posts)