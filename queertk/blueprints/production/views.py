from flask import render_template, url_for
from flask_login import current_user
from .production import bp_productions

# Import remote models
from queertk.blueprints.artist.models import Artist
from queertk.blueprints.common.models import Credit, Season, Notice, NoticeType

# Import local models
from .models import Production, Performance, ProductionNotice

# Import database object
from queertk.database import Session

@bp_productions.route("/<int:prod_id>/<string:slug>")
def display_production(prod_id, slug):

    # TODO A billion queries to get required details from related model -- fix later
    production = Session.begin().query(Production).filter_by(production_id = prod_id).one()
    season = Session.begin().query(Season).filter_by(season_id = production.season_id).one()
    performances = Session.begin().query(Performance).filter_by(production_id = production.production_id).all()
    credits = Session.begin().query(Credit.role, Credit.credit_name, Artist.artist_id).\
        select_from(Credit).\
            join(Artist, Artist.artist_id == Credit.artist_id).\
                filter(Credit.production_id == production.production_id).\
                    all()
    notices = Session.begin().query(ProductionNotice, Notice, NoticeType).select_from(ProductionNotice).join(Notice).join(NoticeType).filter(ProductionNotice.production_id == production.production_id).all()
    
    # TODO Eventually we'll need to make this dynamic 
    poster = url_for('productions.static', filename='images/posters/poster-small.png')

    # Somehow this restricts valid pages to those with a valid slug
    slug = production.slug

    # If production has a poster, set variable to be passed - if not, set to None to avoid passing a nonexistant variable
    if production.poster:
        poster_filename = 'images/posters/' + production.poster
    else:
        poster_filename = None

    return render_template('production.html', title = production.description, 
                                                poster = poster_filename, 
                                                sidebar = True,
                                                current_user = current_user, 
                                                production = production, 
                                                season = season, 
                                                performances = performances, 
                                                credits = credits, 
                                                notices = notices)