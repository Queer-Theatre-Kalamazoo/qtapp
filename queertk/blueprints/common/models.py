# Fixed circular import, ignore warnings
import queertk.blueprints.production.models as prod

# Import utilities
from queertk.models import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String

# Import database object
from queertk.database import db


metadata = Base.metadata

class Credit(Base):
    __tablename__ = 'credits'

    credit_id = Column(Integer, primary_key=True)
    artist_id = Column(Integer, ForeignKey('artists.artist_id'), nullable=False, index=True)
    performance_id = Column(Integer, ForeignKey('performances.performance_id'), index=True)
    production_id = Column(Integer, ForeignKey('productions.production_id'), nullable=False, index=True)
    order_no = Column(Integer)
    category = Column(String(20))
    role = Column(String(100), nullable=False)
    credit_name = Column(String(100), nullable=False)

    def __repr__(self):
        return self.credit_name + " in " + db.session.query(prod.Production).filter_by(production_id = self.production_id).one().description + " as " + self.role

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

class Play(Base):
    __tablename__ = 'plays'

    play_id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255), nullable=False)
    productions = db.relationship('Production', backref = 'Play')

    def __repr__(self):
        return self.title + " by " + self.author

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
