from MySQLdb import Date
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from flask_admin.form import DateTimePickerWidget
from database import db

Base = declarative_base()
metadata = Base.metadata

class Artist(Base):
    __tablename__ = 'artists'

    artist_id = Column(Integer, primary_key=True)
    artist_name = Column(String(100), nullable=False)
    legal_name = Column(String(100))
    short_name = Column(String(100))
    birthday = Column(DateTime)
    biography = Column(Text)
    slug = Column(String(100))
    credits = db.relationship('Credit', backref = 'Artist')

    def __repr__(self):
        return self.artist_name


class Credit(Base):
    __tablename__ = 'credits'

    credit_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'), nullable=False, index=True)
    performance_id = Column(Integer, ForeignKey('performances.performance_id'), index=True)
    production_id = Column(Integer, ForeignKey('productions.production_id'), nullable=False, index=True)
    role = Column(String(100), nullable=False)
    credit_name = Column(String(100), nullable=False)

    def __repr__(self):
        return self.credit_name + " in " + db.session.query(Production).filter_by(production_id = self.production_id).one().description + " as " + self.role


class NoticeType(Base):
    __tablename__ = 'notice_types'

    notice_type_id = Column(Integer, primary_key=True)
    description = Column(String(100), nullable=False)
    notices = db.relationship('Notice', backref = "Type")

    def __repr__(self):
        return self.description


class Notice(Base):
    __tablename__ = 'notices'

    notice_id = Column(Integer, primary_key=True)
    type_id = Column(Integer, ForeignKey('notice_types.notice_type_id'), nullable=False, index=True)
    description = Column(String(200))
    content = Column(String(500), nullable=False)
    notices = db.relationship('ProductionNotice', backref = 'Notice')

    def __repr__(self):
        return self.description


class Performance(Base):
    __tablename__ = 'performances'

    performance_id = Column(Integer, primary_key=True)
    production_id = Column(Integer, ForeignKey('productions.production_id'), nullable=False, index=True)
    venue_id = Column(Integer, ForeignKey('venues.venue_id'), nullable=False, index=True)
    datetime = Column(DateTime, nullable=False)
    credits = db.relationship('Credit', backref = 'Performance')
    notices = db.relationship('ProductionNotice', backref = 'Performance')

    def __repr__(self):
        return str(self.production_id) + " - " + str(self.datetime)


class Play(Base):
    __tablename__ = 'plays'

    play_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    productions = db.relationship('Production', backref = 'Play')

    def __repr__(self):
        return self.title + " by " + self.author


class ProductionNotice(Base):
    __tablename__ = 'production_notices'

    notice_id = Column(Integer, ForeignKey('notices.notice_id'), primary_key=True, nullable=False, index=True)
    production_id = Column(Integer, ForeignKey('productions.production_id'), primary_key=True, nullable=False, index=True)
    performance_id = Column(Integer, ForeignKey('performances.performance_id'), index=True)

    def __repr__(self):
        return db.session.query(Production).filter_by(production_id = self.production_id).one().description + " - " + db.session.query(Notice).filter_by(notice_id = self.notice_id).one().description

class Season(Base):
    __tablename__ = 'seasons'

    season_id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    productions = db.relationship('Production', backref = 'Season')

    def __repr__(self):
        return self.description

class Production(Base):
    __tablename__ = 'productions'

    production_id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.season_id'), nullable=False, index=True)
    play_id = Column(Integer, ForeignKey('plays.play_id'), nullable=False, index=True)
    credits = db.relationship('Credit', backref = 'Production')
    notices = db.relationship('ProductionNotice', backref = 'Production')
    performances = db.relationship('Performance', backref = 'Production')

    def __repr__(self):
        return str(db.session.query(Season).filter_by(season_id = self.season_id).one().description) + " - " + self.description

class Venue(Base):
    __tablename__ = 'venues'

    venue_id = Column(Integer, primary_key=True)
    building = Column(String(255), nullable=False)
    room = Column(String(255))
    address = Column(String(255), nullable=False)
    performances = db.relationship('Performance', backref = 'Venue')

    def __repr__(self):
        if self.room:
            return self.building + " - " + self.room
        else:
            return self.building