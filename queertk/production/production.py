from flask import Blueprint, render_template
from sqlalchemy import or_
from flask_login import current_user, login_required

# Create blueprint
bp_productions = Blueprint("productions", __name__, static_folder = "static", template_folder = "templates", url_prefix = "/prod") # Create Blueprint

from queertk.models import Production, ProductionNotice, Notice, NoticeType, Season, Credit, Performance
from database import db

@bp_productions.route("/<int:prod_id>/<string:slug>")
@login_required
def display_production(prod_id, slug):
    production = db.session.query(Production).filter_by(production_id = prod_id).one()
    season = db.session.query(Season).filter_by(season_id = production.season_id).one()
    performances = db.session.query(Performance).filter_by(production_id = production.production_id).all()
    credits = db.session.query(Credit).filter_by(production_id = production.production_id).all()
    notices = db.session.query(ProductionNotice, Notice, NoticeType).select_from(ProductionNotice).join(Notice).join(NoticeType).filter(ProductionNotice.production_id == production.production_id).all()
    
    # Somehow this restricts valid pages to those with a valid slug
    slug = production.slug

    return render_template('production.html', current_user = current_user, production = production, season = season, performances = performances, credits = credits, notices = notices)