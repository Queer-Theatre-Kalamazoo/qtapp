from flask import Blueprint, render_template, url_for
from sqlalchemy import or_
from flask_login import current_user, login_required

# Create blueprint
bp_productions = Blueprint("productions", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/prod") # Create Blueprint

from queertk.models import Production, ProductionNotice, Notice, NoticeType, Season, Credit, Performance
from queertk.artist.models import Artist
from database import db

@bp_productions.route("/<int:prod_id>/<string:slug>")
def display_production(prod_id, slug):

    # TODO A billion queries to get required details from related model -- fix later
    production = db.session.query(Production).filter_by(production_id = prod_id).one()
    season = db.session.query(Season).filter_by(season_id = production.season_id).one()
    performances = db.session.query(Performance).filter_by(production_id = production.production_id).all()
    credits = db.session.query(Credit.role, Credit.credit_name, Artist.artist_id).\
        select_from(Credit).\
            join(Artist, Artist.artist_id == Credit.artist_id).\
                filter(Credit.production_id == production.production_id).\
                    all()
    notices = db.session.query(ProductionNotice, Notice, NoticeType).select_from(ProductionNotice).join(Notice).join(NoticeType).filter(ProductionNotice.production_id == production.production_id).all()
    
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
