# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy() # Instantiate SQLAlchemy app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from application import app

db_conn_string = app.config.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(db_conn_string, future=True)
Session = sessionmaker(engine, future=True)
