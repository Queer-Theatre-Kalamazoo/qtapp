from flask import render_template
from queertk import app
from queertk.database import Session
from queertk.blueprints.common.models import Season
from queertk.blueprints.production.models import Production
from queertk.blueprints.post.models import Post

@app.route('/')
def home():
    return render_template('index.html', title = 'Home')

@app.route('/events')
def events():
    productions = Session.begin().query(Production.description.label('prod_desc'), Production.slug, Production.production_id, Season.description.label("season_desc")).join(Season, Season.season_id == Production.season_id).filter_by(season_id = 1).all()

    return render_template('events.html', title = 'Events', productions = productions)

@app.route('/news')
def news():
    posts = Session.begin().query(Post).all()
    return render_template('news.html', title = 'News', posts = posts)