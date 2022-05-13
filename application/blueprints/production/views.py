from flask import render_template, url_for
from flask_login import current_user
from .production import bp_productions

# Import remote models
from application.blueprints.common.schema import Artist, Credit, Season, Notice, NoticeType, Production, ProductionNotice, Performance

# Import database object
from application.database import Session
from sqlalchemy import select
from flask_breadcrumbs import register_breadcrumb


@bp_productions.route("/<int:prod_id>/<string:slug>")
@register_breadcrumb(bp_productions, '.', 'Events')
def display_production(prod_id, slug):
    with Session.begin() as session:

        # TODO A billion queries to get required details from related model -- fix later
        production = (
            session.execute(
                select(Production).where(Production.production_id == prod_id)
            )
            .scalars()
            .one()
        )
        season = (
            session.execute(
                select(Season).where(Season.season_id == production.season_id)
            )
            .scalars()
            .one()
        )

        performances = (
            session.execute(
                select(Performance).where(
                    Performance.production_id == production.production_id
                )
            )
            .scalars()
            .all()
        )

        credits = session.execute(
            select(Credit.role, Credit.credit_name, Artist.artist_id)
            .select_from(Credit)
            .where(Credit.production_id == production.production_id)
            .join(Artist)
        ).all()

        notices = session.execute(
            select(ProductionNotice, Notice, NoticeType)
            .select_from(ProductionNotice)
            .where(ProductionNotice.production_id == production.production_id)
            .join(Notice)
            .join(NoticeType)
        ).all()

        # TODO Eventually we'll need to make this dynamic
        poster = url_for(
            "productions.static", filename="images/posters/poster-small.png"
        )

        # Somehow this restricts valid pages to those with a valid slug
        slug = production.slug

        # If production has a poster, set variable to be passed - if not, set to None to avoid passing a nonexistant variable
        if production.poster:
            poster_filename = "images/posters/" + production.poster
        else:
            poster_filename = None

        return render_template(
            "production.html",
            title=production.description,
            poster=poster_filename,
            sidebar=True,
            current_user=current_user,
            production=production,
            season=season,
            performances=performances,
            credits=credits,
            notices=notices,
        )
