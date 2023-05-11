from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import declarative_base
from os import environ

engine = create_engine(
    environ['DATABASE_URI']
)

Session = sessionmaker(bind=engine)
Base = declarative_base()
