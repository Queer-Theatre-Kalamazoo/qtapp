from flask import render_template
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
from sqlalchemy import select, and_


@bp_production.route("/<int:prod_id>")
@bp_production.route("/<int:prod_id>/<string:slug>")
def display_production(prod_id, **slug):
    with Session.begin() as session:

        # TODO A billion queries to get required details from related model
        production = (
            session.execute(select(
                                Production.production_id,
                                Production.title,
                                Production.description,
                                Production.slug,
                                Production.poster,
                                Production.ploxel_iframe,
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

        title_credits = session.execute(
            select(Credit.role, Credit.credit_name, Artist.artist_id, Artist.slug, Artist.headshot)
            .select_from(Credit)
            .where(and_(Credit.production_id == production.production_id, Credit.title_credit == True))
            .outerjoin(Artist)
        ).all()

        cast = session.execute(
            select(Credit.role, Credit.credit_name, Artist.artist_id, Artist.slug, Artist.headshot)
            .select_from(Credit)
            .where(and_(Credit.production_id == production.production_id, Credit.category == "Cast"))
            .outerjoin(Artist)
        ).all()

        crew = session.execute(
            select(Credit.role, Credit.credit_name, Artist.artist_id, Artist.slug, Artist.headshot)
            .select_from(Credit)
            .where(and_(Credit.production_id == production.production_id, Credit.category == "Crew"))
            .outerjoin(Artist)
        ).all()

        director = session.execute(
            select(Credit.credit_name, Credit.artist_id).where(and_(Credit.production_id == production.production_id, Credit.role == "Director"))
        ).one()

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
            title=production.title,
            poster=poster_filename,
            sidebar=True,
            current_user=current_user,
            production=production,
            performances=performances,
            title_credits=title_credits,
            cast=cast,
            crew=crew,
            director=director,
            notices=notices,
        )
