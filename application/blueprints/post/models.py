from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from application.models import Base

metadata = Base.metadata


class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True)
    author_id = Column(
        Integer, ForeignKey("artists.artist_id"), nullable=False, index=True
    )
    title = Column(String(100), nullable=False)
    subtitle = Column(String(50))
    content = Column(Text)
    create_date = Column(DateTime)
    last_updated = Column(DateTime)

    def __repr__(self):
        return self.title
