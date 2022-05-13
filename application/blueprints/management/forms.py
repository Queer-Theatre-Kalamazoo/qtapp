from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectField

# Import models
from application.blueprints.common.schema import Artist

from application.database import Session
from sqlalchemy import select

# Query all artists
# artist_query = Artist.query
def artist_select_query():
    with Session.begin() as session:
        return session.query(Artist).order_by(Artist.artist_name)


class ManagePostForm(FlaskForm):
    author = QuerySelectField(
        "Author", validators=[DataRequired()], query_factory=artist_select_query
    )
    title = StringField(
        "Title",
        validators=[DataRequired(), Length(1, 100, "No more than 100 characters.")],
    )
    subtitle = StringField(
        "Subtitle", validators=[Length(1, 50, "No more than 50 characters.")]
    )
    content = TextAreaField("Content")
