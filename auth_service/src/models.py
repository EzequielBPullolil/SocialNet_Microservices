from sqlalchemy import Column, Integer, String, DateTime
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


Base.metadata.create_all(engine)
