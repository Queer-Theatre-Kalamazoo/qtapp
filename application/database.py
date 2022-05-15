from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import current_app
# from application import app

db_conn_string = current_app.config.get('SQLALCHEMY_DATABASE_URI')
engine = create_engine(db_conn_string, future=True)
Session = sessionmaker(engine, future=True)
