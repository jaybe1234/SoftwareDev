import sys
from sqlalchemy import Column , ForeignKey , Integer , String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy	 import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    name = Column(String(80),nullable = False)
    id = Column(Integer, primary_key = True)
    #password = Column(String(80),nullable = False)
class Password(Base):
    __tablename__ = 'password'
    password = Column(String(80),nullable = False)
    password_id = Column(Integer,ForeignKey('user.id'))
    id = Column(Integer,primary_key = True)
    user = relationship(User)

engine = create_engine('sqlite:///account.db')
Base.metadata.create_all(engine)
