import sys
from sqlalchemy import Column , ForeignKey , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy	 import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    user = Column(String(80),nullable = False)
    id = Column(Integer, primary_key = True)
    #password = Column(String(80),nullable = False)

class Password(Base):
    __tablename__ = 'password'
    password = Column(String(80),nullable = False)
    password_id = Column(Integer,ForeignKey('user.id'))
    password_relationship = relationship(User)

class Name_lecturer(Base):
    __tablename__ = 'name_lecturer'
    namelecturer = Column(String(80),nullable = False)
    namelecturer_id = Column(Integer,ForeignKey('user.id'))
    namelecturer_relationship = relationship(User)

engine = create_engine('sqlite:///lecturer.db')
Base.metadata.create_all(engine)
