from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL
from flask import current_app
# from application import app

# db_conn_string = current_app.config.get('SQLALCHEMY_DATABASE_URI')

db_conn_string = URL.create(
    drivername = 'mysql+mysqlconnector',
    username = current_app.config.get('DATABASE_USER'),
    password = current_app.config.get('DATABASE_PASSWORD'),
    host = current_app.config.get('DATABASE_HOST'),
    database = current_app.config.get('DATABASE_DB')
)

engine = create_engine(db_conn_string, future=True)
Session = sessionmaker(engine, future=True)
