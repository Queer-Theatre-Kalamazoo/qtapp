from flask import render_template, redirect, url_for
from flask import current_app
from application.database import Session
from application.blueprints.common.schema import Season, Production, Post, Person, Relationship, Artist, Credit, Performance
from sqlalchemy import select, and_, func, desc
from application.forms import ContactUsForm
from flask_mail import Message

@current_app.route('/')
def home():
    with Session.begin() as session:
        # Get next performance's production
        query = select(Performance).where(Performance.datetime > func.now()).order_by(Performance.datetime.asc())
        perf = session.execute(query).scalars().first()
        prod = session.execute(select(Production.production_id, Production.slug, Production.title, Production.description).where(Production.production_id == perf.production_id)).one()
        date_range = Production.get_date_range(prod)
        return render_template('index.html', title='Home', next_prod=prod, prod_date_range=date_range)


@current_app.route('/events')
def events():
    with Session.begin() as session:
        query_productions = select(
                        Production.title,
                        Production.slug,
                        Production.poster,
                        Production.production_id).\
                            where(Season.season_id == 1)
        just_productions = session.execute(query_productions).all()

        prod_ids = select(Production.production_id).where(Season.season_id == 1).subquery()

        query_prod = select(
            Production, 
            func.min(Performance.datetime).label("first_perf")
            ).select_from(Production).where(Production.production_id.in_(prod_ids)
            ).group_by(Production.production_id).order_by(desc("first_perf")).join(Performance).subquery()
        productions = session.query(query_prod)
        for p in productions:
            print(p)

        query_title_credits = select(
                                Credit.role, 
                                Credit.credit_name,
                                Credit.production_id, 
                                Artist.artist_id, 
                                Artist.slug, 
                                Artist.headshot
                ).select_from(Credit).where(
                    and_(
                        Credit.title_credit == True, 
                        Credit.production_id.in_(prod_ids)
                        )
                ).outerjoin(Artist).subquery()
        title_credits = session.query(query_title_credits)

        query_directors = select(
                            Credit.credit_name,
                            Credit.artist_id,
                            Credit.production_id
                        ).where(and_(Credit.role == "Director", Credit.production_id.in_(prod_ids))).subquery()
        directors = session.query(query_directors)

        query_performances = select(
                                Performance.production_id,
                                func.min(Performance.datetime).label('open_date'),
                                func.max(Performance.datetime).label('close_date')
                            ).where(Performance.production_id.in_(prod_ids)).group_by(Performance.production_id).subquery()
        performances = session.query(query_performances)

        
        return render_template('events.html', title='Events', productions=productions, performances=performances, directors=directors, title_credits=title_credits)



@current_app.route('/about')
def about():
    with Session.begin() as session:
        with Session.begin() as session:
            staff = session.execute(
                select(Person.name, Person.person_id, Person.artist_id, Relationship.title).select_from(Person).where(and_(Relationship.type == "Staff", Relationship.show_online == True)).join(Relationship, Relationship.person_id == Person.person_id)).all()
            board = session.execute(
                select(Person.name, Person.person_id, Person.artist_id, Relationship.title).select_from(Person).where(and_(Relationship.type == "Board", Relationship.show_online == True)).join(Relationship, Relationship.person_id == Person.person_id)).all()
            
            def get_artist_headshot(artist_id):
                artist = session.execute(
                                    select(Artist.headshot).where(Artist.artist_id == artist_id)
                                    ).one()
                return artist.headshot
        return render_template('about.html', title="About Us", staff=staff, board=board, get_headshot=get_artist_headshot)


@current_app.route("/contact", methods = ['GET', 'POST'])
def contact_us():
    form = ContactUsForm()
    if form.validate_on_submit():
        print(f"Subject: { form.subject.data }, Message: { form.message.data }")

        msg = Message(form.subject.data, recipients=["hazel@queertk.org"])
        msg.html = f'<p>Sender Name: { form.name.data }</p><p>Sender Email: { form.email.data }</p><p>Message: { form.message.data }</p>'
        current_app.mail.send(msg)

        return redirect(url_for('contact_us'))

    return render_template('contact.html', title = 'Contact Us', form = form)