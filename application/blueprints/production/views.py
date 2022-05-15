from flask import render_template
from flask_login import current_user
from . import bp_production

# Import remote models
from application.blueprints.common.schema import (
    Artist,
    Credit,
    Season,
    Notice,
    NoticeType,
    Production,
    ProductionNotice,
    Performance,
)

# Import database object
from application.database import Session
from sqlalchemy import select

@bp_production.route("/<int:prod_id>")
@bp_production.route("/<int:prod_id>/<string:slug>")
def display_production(prod_id, **slug):
    with Session.begin() as session:

        # TODO A billion queries to get required details from related model
        production = (
            session.execute(select(
                                Production.production_id,
                                Production.description,
                                Production.slug,
                                Production.poster,
                                Season.description.label('season_description')
                                )
                            .where(Production.production_id == prod_id).
                            join(Season, Season.season_id == Production.season_id)
                            ).one()
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
            performances=performances,
            credits=credits,
            notices=notices,
        )
