from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from src import Base, engine

from datetime import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime)

    def __init__(self, name, email, password):
        date_current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.name = name
        self.email = email
        self.password = password
        self.created_at = date_current_time


class AuthToken(Base):
    __tablename__ = 'auth_token'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer,
                     ForeignKey('users.id'))
    created_at = Column(DateTime)
    token = Column(String)

    def __init__(self, user_id, token):
        date_current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.created_at = date_current_time
        self.user_id = user_id
        self.token = token


Base.metadata.create_all(engine)
