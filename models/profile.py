from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Profile(Base):
    __tablename__ = 'profiles'

    userid = Column(String(50), primary_key=True)
    created = Column(String(50))
    username = Column(String(50))
    firstname = Column(String(50))
    lastname = Column(String(50))
    gender = Column(String(20))
    age = Column(Integer)
    biography = Column(String(255))
    image = Column(String(255))
