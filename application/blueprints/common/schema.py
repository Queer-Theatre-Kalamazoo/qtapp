# Fixed circular import, ignore warnings
import application.blueprints.common.schema as schema

# Import utilities
from application.models import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text, Boolean, Date, select

from sqlalchemy.orm import relationship
from application.database import Session

from flask import url_for


metadata = Base.metadata


class Artist(Base):
    __tablename__ = 'artists'

    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String(100), nullable=False)
    legal_name = Column(String(100))
    short_name = Column(String(100))
    birthday = Column(DateTime)
    biography = Column(Text)
    headshot = Column(String(100))
    slug = Column(String(100))
    credits = relationship('Credit', backref='Artist')
    posts = relationship('Post', backref='Author')
    
    def get_url(self):
        return url_for('bp_person.display_artist', artist_id=self.artist_id)

    def __repr__(self):
        return self.artist_name


class Credit(Base):
    __tablename__ = "credits"

    credit_id = Column(Integer, primary_key=True)
    artist_id = Column(
        Integer, ForeignKey("artists.artist_id"), nullable=False, index=True
    )
    performance_id = Column(
        Integer, ForeignKey("performances.performance_id"), index=True
    )
    production_id = Column(
        Integer, ForeignKey("productions.production_id"), nullable=False, index=True
    )
    order_no = Column(Integer)
    category = Column(String(20))
    role = Column(String(100), nullable=False)
    credit_name = Column(String(100), nullable=False)

    def __repr__(self):
        with Session.begin() as session:
            return (
                self.credit_name
                + " in "
                + session.query(schema.Production)
                .filter_by(production_id=self.production_id)
                .one()
                .description
                + " as "
                + self.role
            )


class NoticeType(Base):
    __tablename__ = "notice_types"

    notice_type_id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)
    notices = relationship("Notice", backref="Type")

    def __repr__(self):
        return self.description


class Notice(Base):
    __tablename__ = "notices"

    notice_id = Column(Integer, primary_key=True)
    type_id = Column(
        Integer, ForeignKey("notice_types.notice_type_id"), nullable=False, index=True
    )
    description = Column(String(200))
    content = Column(String(500), nullable=False)
    notices = relationship("ProductionNotice", backref="Notice")

    def __repr__(self):
        return self.description


class Person(Base):
    __tablename__ = "people"

    person_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'))
    name = Column(String(100), nullable=False)

    def get_url(self):
        return url_for('bp_person.display_person', person_id=self.person_id)


class Relationship(Base):
    __tablename__ = "relationships"

    relationship_id = Column(Integer, primary_key=True)
    person_id = Column(Integer, ForeignKey('Person.person_id'), nullable=False)
    type = Column(String(20), nullable=False)
    title = Column(String(50))
    show_online = Column(Boolean, nullable=False, default=False)
    start_date = Column(Date)
    end_date = Column(Date)


class Play(Base):
    __tablename__ = "plays"

    play_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    productions = relationship("Production", backref="Play")

    def __repr__(self):
        return self.title + " by " + self.author


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, autoincrement=True)
    author_id = Column(
        Integer, ForeignKey("artists.artist_id"), nullable=False, index=True
    )
    type = Column(String(50))
    title = Column(String(100), nullable=False)
    subtitle = Column(String(50))
    content = Column(Text)
    create_date = Column(DateTime)
    last_updated = Column(DateTime)

    def __repr__(self):
        return self.title


class Performance(Base):
    __tablename__ = "performances"

    performance_id = Column(Integer, primary_key=True)
    production_id = Column(
        Integer, ForeignKey("productions.production_id"), nullable=False, index=True
    )
    venue_id = Column(
        Integer, ForeignKey("venues.venue_id"), nullable=False, index=True
    )
    datetime = Column(DateTime, nullable=False)
    credits = relationship("Credit", backref="Performance")
    notices = relationship("ProductionNotice", backref="Performance")

    def __repr__(self):
        return str(self.production_id) + " - " + str(self.datetime)


class ProductionNotice(Base):
    __tablename__ = "production_notices"

    notice_id = Column(
        Integer,
        ForeignKey("notices.notice_id"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    production_id = Column(
        Integer,
        ForeignKey("productions.production_id"),
        primary_key=True,
        nullable=False,
        index=True,
    )
    performance_id = Column(
        Integer, ForeignKey("performances.performance_id"), index=True
    )

    def __repr__(self):
        with Session.begin() as session:
            return (
                session.execute(
                    select(Production).where(
                        Production.production_id == self.production_id
                    )
                )
                .scalars()
                .one()
                .description
                + " - "
                + session.query(schema.Notice)
                .filter_by(notice_id=self.notice_id)
                .one()
                .description
            )


class Production(Base):
    __tablename__ = "productions"

    production_id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    season_id = Column(
        Integer, ForeignKey("seasons.season_id"), nullable=False, index=True
    )
    play_id = Column(Integer, ForeignKey("plays.play_id"), nullable=False, index=True)
    poster = Column(String(100))
    credits = relationship("Credit", backref="Production")
    notices = relationship("ProductionNotice", backref="Production")
    performances = relationship("Performance", backref="Production")

    def get_url(self):
        return url_for('bp_production.display_production', prod_id=self.production_id, slug=self.slug)

    def __repr__(self):
        with Session.begin() as session:
            return (
                str(
                    session.execute(
                        select(schema.Season).where(
                            schema.Season.season_id == self.season_id
                        )
                    )
                    .scalars()
                    .one()
                    .description
                )
                + " - "
                + self.description
            )


class Season(Base):
    __tablename__ = "seasons"

    season_id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    productions = relationship("Production", backref="Season")

    def __repr__(self):
        return self.description


class Venue(Base):
    __tablename__ = "venues"

    venue_id = Column(Integer, primary_key=True)
    building = Column(String(255), nullable=False)
    room = Column(String(255))
    address = Column(String(255), nullable=False)
    performances = relationship("Performance", backref="Venue")

    def __repr__(self):
        if self.room:
            return self.building + " - " + self.room
        else:
            return self.building
