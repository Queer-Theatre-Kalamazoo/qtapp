# from flask_sqlalchemy import SQLAlchemy
# db = SQLAlchemy() # Instantiate SQLAlchemy app

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_conn_string = 'mysql+mysqlconnector://jpfao9vyo8q9:pscale_pw_XMiOc0SAIOe1mfZbXgVvxrWbjtye7xFsIG3iM_R2q90@pylkzqxt5vhc.us-east-1.psdb.cloud/qtdb'
engine = create_engine(db_conn_string, future=True)
Session = sessionmaker(engine, future=True)
