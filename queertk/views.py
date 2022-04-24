from flask import render_template
from queertk import app
from database import db
from queertk.blueprints.common.models import Season
from queertk.production.models import Production
from queertk.post.models import Post

@app.route('/')
def home():
    return render_template('index.html', title = 'Home')

@app.route('/events')
def events():
    productions = db.session.query(Production.description.label('prod_desc'), Production.slug, Production.production_id, Season.description.label("season_desc")).join(Season, Season.season_id == Production.season_id).filter_by(season_id = 1).all()

    return render_template('events.html', title = 'Events', productions = productions)

@app.route('/news')
def news():
    posts = db.session.query(Post).all()
    return render_template('news.html', title = 'News', posts = posts)