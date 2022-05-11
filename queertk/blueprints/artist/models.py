from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from queertk.models import Base
from sqlalchemy.orm import relationship

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
    credits = relationship('Credit', backref = 'Artist')
    posts = relationship('Post', backref = 'Author')

    def __repr__(self):
        return self.artist_name