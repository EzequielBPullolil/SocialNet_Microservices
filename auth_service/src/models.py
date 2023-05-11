from sqlalchemy import Column, Integer, String, DateTime
from src import Base, engine


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    created_at = Column(DateTime)

    def __init__(self, name, email, password, created_at):
        self.name = name
        self.email = email
        self.password = password
        self.created_at = created_at


Base.metadata.create_all(engine)
