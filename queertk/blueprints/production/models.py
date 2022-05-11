# Fixed circular import error
import queertk.blueprints.common.models as common

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from queertk.database import Session
from queertk.models import Base

metadata = Base.metadata

class Performance(Base):
    __tablename__ = 'performances'

    performance_id = Column(Integer, primary_key=True)
    production_id = Column(Integer, ForeignKey('productions.production_id'), nullable=False, index=True)
    venue_id = Column(Integer, ForeignKey('venues.venue_id'), nullable=False, index=True)
    datetime = Column(DateTime, nullable=False)
    credits = relationship('Credit', backref = 'Performance')
    notices = relationship('ProductionNotice', backref = 'Performance')

    def __repr__(self):
        return str(self.production_id) + " - " + str(self.datetime)

class ProductionNotice(Base):
    __tablename__ = 'production_notices'

    notice_id = Column(Integer, ForeignKey('notices.notice_id'), primary_key=True, nullable=False, index=True)
    production_id = Column(Integer, ForeignKey('productions.production_id'), primary_key=True, nullable=False, index=True)
    performance_id = Column(Integer, ForeignKey('performances.performance_id'), index=True)

    def __repr__(self):
        with Session.begin() as session:
            return session.query(Production).filter_by(production_id = self.production_id).one().description + " - " + session.query(common.Notice).filter_by(notice_id = self.notice_id).one().description

class Production(Base):
    __tablename__ = 'productions'

    production_id = Column(Integer, primary_key=True)
    description = Column(String(255), nullable=False)
    slug = Column(String(100), nullable=False)
    season_id = Column(Integer, ForeignKey('seasons.season_id'), nullable=False, index=True)
    play_id = Column(Integer, ForeignKey('plays.play_id'), nullable=False, index=True)
    poster = Column(String(100))
    credits = relationship('Credit', backref = 'Production')
    notices = relationship('ProductionNotice', backref = 'Production')
    performances = relationship('Performance', backref = 'Production')

    def __repr__(self):
        with Session.begin() as session:
            return str(session.query(common.Season).filter_by(season_id = self.season_id).one().description) + " - " + self.description